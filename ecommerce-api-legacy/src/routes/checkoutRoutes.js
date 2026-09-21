const express = require('express');
const CheckoutController = require('../controllers/CheckoutController');

const router = express.Router();

router.post('/checkout', CheckoutController.handleCheckout);

module.exports = router;
