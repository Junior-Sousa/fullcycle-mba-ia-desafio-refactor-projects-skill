const ReportService = require('../services/ReportService');

class ReportController {
    static async handleFinancialReport(req, res) {
        try {
            const report = await ReportService.generateFinancialReport();
            return res.status(200).json(report);
        } catch (error) {
            return res.status(500).send("Erro DB");
        }
    }
}

module.exports = ReportController;
