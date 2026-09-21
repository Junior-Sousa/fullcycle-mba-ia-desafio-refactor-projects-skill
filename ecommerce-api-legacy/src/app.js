const express = require('express');
const { config } = require('./config/settings');
const { initDb } = require('./database/connection');
const checkoutRoutes = require('./routes/checkoutRoutes');
const reportRoutes = require('./routes/reportRoutes');
const userRoutes = require('./routes/userRoutes');

const app = express();
app.use(express.json());

app.use('/api', checkoutRoutes);
app.use('/api', reportRoutes);
app.use('/api', userRoutes);

initDb().then(() => {
    if (require.main === module) {
        app.listen(config.port, () => {
            console.log(`E-Commerce API rodando na porta ${config.port}...`);
        });
    }
}).catch(err => {
    console.error("Erro ao inicializar banco de dados:", err);
});

module.exports = app;
