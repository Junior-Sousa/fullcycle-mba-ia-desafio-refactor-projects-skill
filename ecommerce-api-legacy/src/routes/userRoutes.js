const express = require('express');
const UserController = require('../controllers/UserController');

const router = express.Router();

router.delete('/users/:id', UserController.deleteUser);

module.exports = router;
