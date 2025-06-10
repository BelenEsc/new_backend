const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

// Middleware setup
app.use(cors({
    origin: 'http://localhost:3000',
    methods: ['POST'],
    allowedHeaders: ['Content-Type']
}));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage });

// API endpoint
app.post('/api/storage-requests', upload.fields([
    { name: 'manifest_file', maxCount: 1 },
    { name: 'sampling_permits_file', maxCount: 1 },
    { name: 'nagoya_permits_file', maxCount: 1 }
]), (req, res) => {
    try {
        const data = req.body;
        const files = req.files;

        // Process the form data and files
        console.log('Received data:', data);
        console.log('Received files:', files);

        // Save to database or process as needed
        res.status(200).json({
            message: 'Form submitted successfully',
            data: data,
            files: files
        });
    } catch (error) {
        console.error('Error processing request:', error);
        res.status(500).json({ error: 'Server error processing request' });
    }
});

// Serve static files
app.use('/uploads', express.static('uploads'));

// Start server
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});