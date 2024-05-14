const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const port = 3000;

app.use(bodyParser.json());

// Define the directory where static files (CSS, JS, etc.) are located.
// app.use(express.static(path.join(__dirname, '/../public')));
app.use(express.static(path.join(__dirname, '/../public__test')));

// Route to serve the index.html file
app.get('/', function(req, res) {
    // res.sendFile(path.join(__dirname, 'index.html'));
    res.sendFile(path.join(__dirname, 'propose.html'));
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

// app.post('/proxy_assistant_mail', async (req, res) => {
//   const url = 'https://mail.kobu.agency'; // Use HTTPS para uma conexão segura

//   try {
//     const response = await axios.post(url, req.body, {
//       headers: {
//         'Content-Type': 'application/json',
//         'Accept': 'application/json',
//       }
//     });

//     // Encaminha a resposta do servidor de e-mail de volta para o cliente
//     res.status(response.status).json(response.data);
//   } catch (error) {
//     // Se ocorrer um erro, envie uma resposta de erro ao cliente
//     console.error('Erro ao enviar e-mail:', error);
//     res.status(500).json({ error: 'Erro ao enviar e-mail' });
//   }
// });


app.listen(port, () => {
  console.log(`Web server running at http://localhost:${port}`);
});
