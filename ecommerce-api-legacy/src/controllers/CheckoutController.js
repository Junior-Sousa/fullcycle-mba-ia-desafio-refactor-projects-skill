const CheckoutService = require('../services/CheckoutService');

class CheckoutController {
    static async handleCheckout(req, res) {
        try {
            const { usr, eml, pwd, c_id, card } = req.body || {};
            const result = await CheckoutService.processCheckout({ usr, eml, pwd, c_id, card });

            if (result.message) {
                return res.status(result.status).send(result.message);
            }

            return res.status(result.status).json(result.data);
        } catch (error) {
            return res.status(500).send("Erro Interno");
        }
    }
}

module.exports = CheckoutController;
