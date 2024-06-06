const express = require('express');
const cors = require('cors');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const port = 3000;
const corsOptions = {       // Coment this line to allow cross origin from not local origins
  origin: 'http://127.0.0.1:5500',
  optionsSuccessStatus: 200
};


app.use(cors(corsOptions)); // Remove corsOptions to allow cross origin from not local origins
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '/../../dist/')));


app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/../../dist/html/index.html'));
});

app.post('/proxy', async (req, res) => {
  // const url = 'https://assistant.kobudev.com/kobu-assistant';
  const url = 'http://127.0.0.1:5000/kobu-assistant';
  try {
    const response = await axios.post(url, req.body, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    });

    res.json(response.data);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Proxy server error' });
  }
});

app.listen(port, () => {
  console.log(`Web server running at http://localhost:${port}`);
});
