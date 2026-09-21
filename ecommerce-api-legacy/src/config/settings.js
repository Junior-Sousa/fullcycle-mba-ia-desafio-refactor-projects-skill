const config = {
    env: process.env.NODE_ENV || 'development',
    port: process.env.PORT || 3000,
    dbUser: process.env.DB_USER || 'admin_master',
    dbPass: process.env.DB_PASS || 'dev_secret_pass',
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'pk_dev_key',
    smtpUser: process.env.SMTP_USER || 'no-reply@fullcycle.com.br'
};

module.exports = { config };
