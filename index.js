const express = require("express");
const app = express();
const path = require("path");

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// Route for the root URL
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start the server
const port = 3000; // Change to the desired port number
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
