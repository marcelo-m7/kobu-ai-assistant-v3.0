module.exports = {
    proxy: "http://localhost:3000",
    files: ["dist/**/*.{html,css,js}"],
    port: 4000,
    open: false,
    ui: false,
    ghostMode: false,
    online: false,
    tunnel: false
  };
  
  console.log("Use the address http://localhost:4000 to access the live server.");
  