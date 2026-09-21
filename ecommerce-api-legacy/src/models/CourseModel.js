const { dbGet, dbAll } = require('../database/connection');

class CourseModel {
    static async findActiveById(id) {
        return await dbGet("SELECT id, title, price, active FROM courses WHERE id = ? AND active = 1", [id]);
    }

    static async findAll() {
        return await dbAll("SELECT id, title, price, active FROM courses");
    }
}

module.exports = CourseModel;
