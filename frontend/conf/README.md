# Frontend Node-Web-Server Repository

**Documentation Update:**

**Please be advised that the repository documentation is currently being updated to provide more accurate and helpful information. We apologize for any inconvenience this may cause and appreciate your patience. If you have any questions or need further assistance, please don't hesitate to reach out. Thank you for your understanding.**

------------------------------------------------------

This repository hosts a straightforward Node.js web server. It serves the frontend on the index route and acts as a proxy on a secondary route for making HTTP requests to the AI Assistant API.

## Installation

Install dependencies:

```bash
npm install
```

## Cross-Origin Deal

If your web server has an HTTPS certificate, you may remove the proxy config. Review the comments within the `Conversation.sendRequest()` method in `js/conversation.js` to enable/disable the proxy to deal with cross-origin security issues. By default, the client requests are sent to the localhost proxy (`const url = 'http://localhost:3000/proxy'`).

Note that the localhost proxy is what actually sends the request to the URL defined in `frontend/src/app.js`, in the default configuration.

If you are using the provided node-server proxy, you may also need to adjust the final URL request destination in the route `/proxy`. Check out the URL set in `frontend/src/app.js`. The default URL set is `const url = 'http://127.0.0.1:5000/kobu-assistant';`.

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

## Configuration

You can configure the server port and other settings in the `app.js` file.

In case of cross-origin issues, you may need to review the comments within the `Conversation.sendRequest()` method in `js/conversation.js`. This is to adjust the configuration of the frontend-backend communication, particularly regarding cross-origin resource sharing (CORS) settings, if needed.

## Dependencies

- [Express](https://www.npmjs.com/package/express): Fast, unopinionated, minimalist web framework for Node.js.
- [Axios](https://www.npmjs.com/package/axios): Promise-based HTTP client for the browser and Node.js.
- [Body-Parser](https://www.npmjs.com/package/body-parser): Node.js body parsing middleware.