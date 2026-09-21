const { dbAll } = require('../database/connection');

class ReportModel {
    static async getFinancialReportData() {
        const sql = `
            SELECT 
                c.id as course_id,
                c.title as course_title,
                c.price as course_price,
                u.name as student_name,
                u.email as student_email,
                p.amount as payment_amount,
                p.status as payment_status
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            LEFT JOIN users u ON e.user_id = u.id
            LEFT JOIN payments p ON e.id = p.enrollment_id
            ORDER BY c.id
        `;
        return await dbAll(sql);
    }
}

module.exports = ReportModel;
