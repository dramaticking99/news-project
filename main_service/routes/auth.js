// routes/auth.js
const express = require('express');
const router = express.Router();
const authService = require('../services/authService'); // Import the service

// @route   POST /api/auth/register
// @desc    Register a new user
router.post('/register', async (req, res) => {
  try {
    // Call the service to handle the business logic
    await authService.registerUser(req.body);
    res.status(201).json({ msg: 'User registered successfully' });
  } catch (err) {
    // Handle errors thrown by the service
    if (err.message === 'User with this email already exists') {
      return res.status(400).json({ msg: err.message });
    }
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST /api/auth/login
// @desc    Authenticate user & get token
router.post('/login', async (req, res) => {
  try {
    // Call the service to handle the login logic
    const token = await authService.loginUser(req.body);
    res.json({ token });
  } catch (err) {
    // Handle errors thrown by the service
    if (err.message === 'Invalid credentials') {
      return res.status(400).json({ msg: err.message });
    }
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;