const UserModel = require('../models/UserModel');

class UserController {
    static async deleteUser(req, res) {
        try {
            const { id } = req.params;
            const deleted = await UserModel.deleteWithCascading(id);
            if (!deleted) {
                return res.status(404).send("Usuário não encontrado");
            }
            return res.status(200).send("Usuário e registros associados deletados com sucesso.");
        } catch (error) {
            return res.status(500).send("Erro ao deletar usuário");
        }
    }
}

module.exports = UserController;
