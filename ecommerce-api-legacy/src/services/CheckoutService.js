const UserModel = require('../models/UserModel');
const CourseModel = require('../models/CourseModel');
const EnrollmentModel = require('../models/EnrollmentModel');
const PaymentModel = require('../models/PaymentModel');
const AuditLogModel = require('../models/AuditLogModel');

class CheckoutService {
    static async processCheckout({ usr, eml, pwd, c_id, card }) {
        if (!usr || !eml || !c_id || !card) {
            return { status: 400, message: "Bad Request" };
        }

        const course = await CourseModel.findActiveById(c_id);
        if (!course) {
            return { status: 404, message: "Curso não encontrado" };
        }

        let user = await UserModel.findByEmail(eml);
        let userId;

        if (!user) {
            userId = await UserModel.create(usr, eml, pwd || "123456");
        } else {
            userId = user.id;
        }

        const paymentStatus = card.startsWith("4") ? "PAID" : "DENIED";
        if (paymentStatus === "DENIED") {
            return { status: 400, message: "Pagamento recusado" };
        }

        const enrollmentId = await EnrollmentModel.create(userId, c_id);
        await PaymentModel.create(enrollmentId, course.price, paymentStatus);
        await AuditLogModel.log(`Checkout curso ${c_id} por ${userId}`);

        return {
            status: 200,
            data: { msg: "Sucesso", enrollment_id: enrollmentId }
        };
    }
}

module.exports = CheckoutService;
