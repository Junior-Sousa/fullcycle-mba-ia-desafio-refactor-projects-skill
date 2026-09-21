const { dbRun } = require('../database/connection');

class AuditLogModel {
    static async log(action) {
        return await dbRun("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [action]);
    }
}

module.exports = AuditLogModel;
