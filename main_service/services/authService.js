const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Registers a new user.
 * @param {object} userData - The user's data (name, email, password).
 * @returns {Promise<object>} The saved user object.
 */
const registerUser = async (userData) => {
  const { name, email, password } = userData;

  // Check if user already exists
  let user = await User.findOne({ email });
  if (user) {
    // Throw an error that the controller will catch
    throw new Error('User with this email already exists');
  }

  user = new User({ name, email, password });

  // Hash the password
  const salt = await bcrypt.genSalt(10);
  user.password = await bcrypt.hash(password, salt);

  // Save the user and return the result
  await user.save();
  return user;
};

/**
 * Logs in a user.
 * @param {object} credentials - The user's credentials (email, password).
 * @returns {Promise<string>} The generated JWT.
 */
const loginUser = async (credentials) => {
  const { email, password } = credentials;

  // Check if user exists
  const user = await User.findOne({ email });
  if (!user) {
    throw new Error('Invalid credentials');
  }

  // Compare passwords
  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) {
    throw new Error('Invalid credentials');
  }

  // Create and sign the JWT
  const payload = { user: { id: user.id } };
  const token = jwt.sign(
    payload,
    process.env.JWT_SECRET,
    { expiresIn: 3600 }
  );

  return token;
};

module.exports = {
  registerUser,
  loginUser,
};