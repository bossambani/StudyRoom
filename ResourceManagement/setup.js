const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const users = []; // In-memory users store for simplicity (use a database in production)

// Set up storage engine
const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const upload = multer({ storage: storage });

// Middleware to serve static files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use(express.static('public'));

// JWT secret
const JWT_SECRET = 'your_jwt_secret_key'; // Use a secure key in production

// User registration
app.post('/register', async (req, res) => {
  const { username, password, role = 'user' } = req.body; // Default role is 'user'
  const hashedPassword = await bcrypt.hash(password, 10);
  users.push({ username, password: hashedPassword, role });
  res.json({ message: 'User registered successfully' });
});

// User login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  const token = jwt.sign({ username, role: user.role }, JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Middleware to authenticate users
const authenticate = (req, res, next) => {
  const token = req.headers['authorization'];
  if (!token) return res.status(403).json({ message: 'No token provided' });
  try {
    const decoded = jwt.verify(token.split(' ')[1], JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(403).json({ message: 'Failed to authenticate token' });
  }
};

// Middleware to authorize based on role
const authorize = (roles = []) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Permission denied' });
    }
    next();
  };
};

// Upload endpoint (requires authentication and 'admin' role)
app.post('/upload', authenticate, authorize(['admin']), upload.single('file'), (req, res) => {
  const { category } = req.body;
  const file = { ...req.file, category };
  res.json({
    message: 'File uploaded successfully',
    file
  });
});

// Endpoint to list all files (available to all authenticated users)
app.get('/files', authenticate, (req, res) => {
  const { category } = req.query;
  fs.readdir('./uploads', (err, files) => {
    if (err) {
      return res.status(500).json({ message: 'Unable to retrieve files' });
    }
    const filteredFiles = category ? files.filter(file => file.includes(category)) : files;
    res.json(filteredFiles);
  });
});

// Delete a file (requires authentication and 'admin' role)
app.delete('/files/:filename', authenticate, authorize(['admin']), (req, res) => {
  const filepath = path.join(__dirname, 'uploads', req.params.filename);
  fs.unlink(filepath, (err) => {
    if (err) {
      return res.status(500).json({ message: 'File not found' });
    }
    res.json({ message: 'File deleted successfully' });
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));

