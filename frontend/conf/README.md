# Frontend Node-Web-Server Repository

This repository hosts a simple Node.js web server. It serves the frontend on the index route and acts as a proxy on a secondary route for making HTTP requests to the AI Assistant API.

## Installation

Install dependencies:

```bash
npm install
```

## Cross-Origin Issue

If your web server has an HTTPS certificate, you may remove the proxy configuration. Review the comments within the `Conversation.sendRequest()` method in `js/conversation.js` to enable/disable the proxy to deal with cross-origin security issues. By default, the client requests are sent to the localhost proxy (`const url = 'http://localhost:3000/proxy'`).

**Choose the interface model in `frontend\dist__test\js\conversation.js`**
```js
    const url = 'http://localhost:3000/proxy'; // Default local proxy (no need to add any URL)
    // const url = 'https://assistant.kobudev.com/kobu-assistant'; // Use this URL if you don't want to use any proxy
```

Note that the localhost proxy is what actually sends the request to the URL defined in `frontend/src/app.js`, in the default configuration.

If you are using the provided node-server proxy, you may also need to adjust the final URL request destination in the route `/proxy`. Check out the URL set in `frontend/src/app.js`. The default URL set is `const url = 'http://127.0.0.1:5000/kobu-assistant';`.

**Choose the interface model in `frontend\src\app.js`**
```js
// Define the directory where static files (CSS, JS, etc.) are located.
// app.use(express.static(path.join(__dirname, '/../dist')));
app.use(express.static(path.join(__dirname, '/../dist__test'))); Recommended (default)
```
**Choose the Assistant API in `frontend\src\app.js`**
```js
app.post('/proxy', async (req, res) => {
  // const url = 'https://assistant.kobudev.com/kobu-assistant'; // KobuDev Server (default)
  const url = 'http://127.0.0.1:5000/kobu-assistant'; // Local (default)
```

## Usage

To start the web server, run the following command:

```bash
npm start
```

Or run the following command to start the server with nodemon watcher enabled (automatically refreshes the server if any alterations in scripts or HTML files):

```bash
npm run dev
```

This will start the server on port 3000 by default.

## Features

- **Static File Serving**: The server serves static files such as HTML, CSS, and JavaScript.
- **Proxy Server**: The server acts as a proxy for making HTTP POST requests to another server (`https://assistant.kobudev.com/kobu-assistant`).

## Dependencies

- [Express](https://www.npmjs.com/package/express): Fast, unopinionated, minimalist web framework for Node.js.
- [Axios](https://www.npmjs.com/package/axios): Promise-based HTTP client for the browser and Node.js.
- [Body-Parser](https://www.npmjs.com/package/body-parser): Node.js body parsing middleware.

## Additional Scripts

- **Browsersync**: Use the following command to start BrowserSync, which will launch the live server:
  ```bash
  npm run browsersync
  ```

- **SCSS Watcher**: Use the following command to compile SCSS files to CSS and watch for changes:
  ```bash
  npm run scss
  ```