const { dbGet, dbRun, dbAll } = require('../database/connection');
const crypto = require('crypto');

class UserModel {
    static hashPassword(password) {
        if (!password) return '';
        return crypto.createHash('sha256').update(password).digest('hex');
    }

    static async findByEmail(email) {
        return await dbGet("SELECT id, name, email, pass FROM users WHERE email = ?", [email]);
    }

    static async findById(id) {
        return await dbGet("SELECT id, name, email FROM users WHERE id = ?", [id]);
    }

    static async create(name, email, password) {
        const hash = this.hashPassword(password);
        const result = await dbRun("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [name, email, hash]);
        return result.lastID;
    }

    static async deleteWithCascading(id) {
        const enrollments = await dbAll("SELECT id FROM enrollments WHERE user_id = ?", [id]);
        for (const enr of enrollments) {
            await dbRun("DELETE FROM payments WHERE enrollment_id = ?", [enr.id]);
        }
        await dbRun("DELETE FROM enrollments WHERE user_id = ?", [id]);
        const res = await dbRun("DELETE FROM users WHERE id = ?", [id]);
        return res.changes > 0;
    }
}

module.exports = UserModel;
