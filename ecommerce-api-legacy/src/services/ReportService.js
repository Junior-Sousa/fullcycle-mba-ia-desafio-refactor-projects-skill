const ReportModel = require('../models/ReportModel');

class ReportService {
    static async generateFinancialReport() {
        const rows = await ReportModel.getFinancialReportData();
        const coursesMap = new Map();

        for (const row of rows) {
            if (!coursesMap.has(row.course_id)) {
                coursesMap.set(row.course_id, {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                });
            }

            const courseEntry = coursesMap.get(row.course_id);
            if (row.student_name) {
                const paidAmount = row.payment_status === 'PAID' ? (row.payment_amount || 0) : 0;
                if (row.payment_status === 'PAID' && row.payment_amount) {
                    courseEntry.revenue += row.payment_amount;
                }
                courseEntry.students.push({
                    student: row.student_name,
                    paid: paidAmount
                });
            }
        }

        return Array.from(coursesMap.values());
    }
}

module.exports = ReportService;
