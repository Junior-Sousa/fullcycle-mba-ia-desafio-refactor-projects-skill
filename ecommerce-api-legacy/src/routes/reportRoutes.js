const express = require('express');
const ReportController = require('../controllers/ReportController');

const router = express.Router();

router.get('/admin/financial-report', ReportController.handleFinancialReport);

module.exports = router;
