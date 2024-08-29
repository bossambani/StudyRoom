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
  const { username, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  users.push({ username, password: hashedPassword });
  res.json({ message: 'User registered successfully' });
});

// User login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username);
  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  const token = jwt.sign({ username }, JWT_SECRET, { expiresIn: '1h' });
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

// Upload endpoint (requires authentication)
app.post('/upload', authenticate, upload.single('file'), (req, res) => {
  const { category } = req.body;
  const file = { ...req.file, category };
  res.json({
    message: 'File uploaded successfully',
    file
  });
});

// Endpoint to list all files (with optional category filtering)
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

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));

