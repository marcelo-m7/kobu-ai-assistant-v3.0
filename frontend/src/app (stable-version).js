const express = require('express');
const app = express();
const path = require('path');

// Define the directory where static files (CSS, JS, etc.) are located.
app.use(express.static(path.join(__dirname, 'static')));

// Route to serve the index.html file
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Starts the server on port 3000
app.listen(3000, () => console.log("Web server running on port 3000."));
