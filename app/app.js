const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();

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

// Upload endpoint
app.post('/upload', upload.single('file'), (req, res) => {
  res.json({
    message: 'File uploaded successfully',
    file: req.file
  });
});

// Endpoint to list all files
app.get('/files', (req, res) => {
  fs.readdir('./uploads', (err, files) => {
    if (err) {
      return res.status(500).json({ message: 'Unable to retrieve files' });
    }
    res.json(files);
  });
});

// Serve files for download
app.get('/download/:filename', (req, res) => {
  const filepath = path.join(__dirname, 'uploads', req.params.filename);
  res.download(filepath);
});

// Delete a file
app.delete('/files/:filename', (req, res) => {
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

