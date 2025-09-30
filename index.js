// index.js

require('dotenv').config();
const express = require('express');
const connectDB = require('./db/connection'); // <-- 1. IMPORT the DB connection

const app = express();

// Connect to the Database
connectDB();

// Middleware to parse JSON
app.use(express.json());

// Any request to /api/auth will be handled by the auth router
app.use('/api/auth', require('./routes/auth'));

// A simple test route
app.get('/', (req, res) => {
  res.send('News Project API is running!');
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});