# Conhecimento: Playbook de Refatoração Arquitetural (Multi-Stack)

Catálogo prático de padrões de transformação arquitetural para migração para o padrão MVC (Model-View-Controller) com Clean Architecture e SOLID. Cada padrão contém contextualização técnica e exemplos práticos de código no formato **Antes (Anti-pattern / Legado)** versus **Depois (Refatorado / MVC Seguro)**.

---

## 1. Extrair Lógica de Dados para Camada de Model / Repository
**Problema**: Rotas ou controladores executam queries SQL brutas diretamente, misturando a camada de transporte com a de persistência de dados.  
**Solução**: Mover o acesso a dados para classes de Model ou Repositórios dedicados, expondo métodos semânticos.

### Exemplo (Python / Flask)
#### ❌ Antes (Query na Rota / Controller)
```python
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    db = sqlite3.connect("loja.db")
    cursor = db.cursor()
    cursor.execute("SELECT id, nome, preco, categoria FROM produtos WHERE ativo = 1")
    produtos = [{"id": r[0], "nome": r[1], "preco": r[2]} for r in cursor.fetchall()]
    db.close()
    return jsonify(produtos)
```

#### ✅ Depois (MVC: Model + Controller + Rota)
```python
# models/produto_model.py
class ProdutoModel:
    @staticmethod
    def listar_ativos():
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT id, nome, preco, categoria FROM produtos WHERE ativo = 1")
            return [dict(row) for row in cursor.fetchall()]

# controllers/produto_controller.py
class ProdutoController:
    @staticmethod
    def index():
        produtos = ProdutoModel.listar_ativos()
        return jsonify(produtos), 200
```

---

## 2. Desacoplar Roteamento de Lógica de Negócio (Thin Controllers)
**Problema**: Handlers de rota concentram validações pesadas, transformações de payload e orquestração de serviços, dificultando testes unitários e reuso.  
**Solução**: Manter as rotas apenas como mapeadores de entrada HTTP e delegar a orquestração para Controllers/Services enxutos.

### Exemplo (Node.js / Express)
#### ❌ Antes (Lógica inline misturada na Rota)
```javascript
app.post("/checkout", async (req, res) => {
    const { userId, courseId, paymentMethod } = req.body;
    if (!userId || !courseId) return res.status(400).send("Campos obrigatórios");
    const user = await db.get("SELECT * FROM users WHERE id = ?", [userId]);
    const course = await db.get("SELECT * FROM courses WHERE id = ?", [courseId]);
    const total = course.price * 0.9; // Regra de desconto chumbada
    await db.run("INSERT INTO enrollments (user_id, course_id, amount) VALUES (?, ?, ?)", [userId, courseId, total]);
    res.json({ success: true, total });
});
```

#### ✅ Depois (MVC: Rotas limpas delegando a Controller e Model)
```javascript
// routes/api.js
router.post("/checkout", CheckoutController.processCheckout);

// controllers/CheckoutController.js
class CheckoutController {
    static async processCheckout(req, res) {
        try {
            const { userId, courseId, paymentMethod } = req.body;
            if (!userId || !courseId) {
                return res.status(400).json({ error: "Dados obrigatórios não informados" });
            }
            const enrollment = await EnrollmentModel.createWithDiscount(userId, courseId, 0.10);
            return res.status(201).json({ success: true, enrollment });
        } catch (error) {
            return res.status(500).json({ error: error.message });
        }
    }
}
```

---

## 3. Centralização Segura de Configurações e Segredos
**Problema**: Chaves de API, senhas de banco e segredos de sessão (`SECRET_KEY`, `JWT_SECRET`) declarados como literais de string no código-fonte.  
**Solução**: Extrair para módulo centralizado (`config/settings`) alimentado exclusivamente por variáveis de ambiente (`os.environ` / `process.env`) com fallbacks seguros para desenvolvimento.

### Exemplo (Python & Node.js)
#### ❌ Antes (Credenciais Hardcoded)
```python
# app.py
app = Flask(__name__)
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123456"
DATABASE_URL = "sqlite:///loja.db"
```

#### ✅ Depois (Configuração Desacoplada)
```python
# src/config/settings.py
import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-key-change-in-prod")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
    DEBUG = os.getenv("FLASK_ENV") != "production"

# src/app.py
from src.config.settings import Settings
app.config["SECRET_KEY"] = Settings.SECRET_KEY
```

---

## 4. Prevenção de SQL Injection com Consultas Parametrizadas
**Problema**: Concatenação ou interpolação de strings para montagem de queries SQL com dados de requisição (`f"WHERE id = {user_id}"`).  
**Solução**: Utilizar placeholders de bind parameters (`?` no SQLite/Python, `$1` no Postgres/Node, ou `:param` no SQLAlchemy/PDO).

### Exemplo (Python / SQLite)
#### ❌ Antes (SQL Concatenado Vulnerável)
```python
def buscar_usuario(email):
    query = f"SELECT * FROM usuarios WHERE email = '{email}'"
    return cursor.execute(query).fetchone()
```

#### ✅ Depois (Query Parametrizada Segura)
```python
def buscar_usuario(email):
    query = "SELECT id, nome, email, role FROM usuarios WHERE email = ?"
    cursor.execute(query, (email,))
    return cursor.fetchone()
```

---

## 5. Endpoint Administrativo de SQL Livre / Execução Arbitrária de Queries
**Problema**: A aplicação disponibiliza um endpoint administrativo (como `POST /admin/query`) que recebe uma string SQL arbitrária no corpo da requisição e a executa diretamente com `cursor.execute(sql)`. Isso representa uma grave falha de segurança (CWE-89 / Injeção Total / Backdoor), permitindo a exclusão total da base de dados (`DROP TABLE`), escalada de privilégios ou extração de dados sensíveis.  
**Solução**: 
1. **Substituição por Endpoints Operacionais Específicos**: Ações administrativas legítimas (ex: reset de dados de teste, expurgo de registros) devem ser encapsuladas em endpoints dedicados e parametrizados (ex: `POST /admin/reset-database`).
2. **Defesa em Profundidade para Endpoints de Consulta**: Se o endpoint de inspeção/consulta for mantido para fins de compatibilidade/relatórios:
   - Bloquear categoricamente comandos destrutivos e mutativos de DDL e DML (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `CREATE`, `ATTACH`, `PRAGMA`).
   - Rejeitar estritamente o encadeamento de múltiplos comandos (bloquear o caractere `;` para impedir *query stacking*).
   - Permitir única e exclusivamente consultas de leitura (`SELECT`) bem-formadas.
   - Retornar erros sem expor detalhes internos do banco de dados.

### Exemplo (Python / Flask)
#### ❌ Antes (Execução Arbitrária e Insegura de SQL)
```python
# controllers/admin_controller.py
@app.route("/admin/query", methods=["POST"])
def executar_query():
    dados = request.get_json()
    query = dados.get("sql", "")
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query) # VULNERABILIDADE CRÍTICA: Executa qualquer comando SQL livre
    if query.strip().upper().startswith("SELECT"):
        return jsonify({"dados": cursor.fetchall()})
    db.commit()
    return jsonify({"mensagem": "Query executada"})
```

#### ✅ Depois (Refatoração Segura com Endpoints Específicos e Bloqueio Restrito)
```python
# controllers/admin_controller.py
class AdminController:
    # 1. Operação administrativa explícita e controlada
    @staticmethod
    def reset_database():
        try:
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM itens_pedido")
                cursor.execute("DELETE FROM pedidos")
                cursor.execute("DELETE FROM produtos")
                cursor.execute("DELETE FROM usuarios")
                db.commit()
            return jsonify({"mensagem": "Banco de dados resetado com sucesso", "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": "Falha ao resetar banco de dados"}), 500

    # 2. Endpoint de inspeção protegido contra execução destrutiva e SQL injection arbitrário
    @staticmethod
    def executar_query():
        dados = request.get_json() or {}
        query = dados.get("sql", "").strip()

        if not query:
            return jsonify({"erro": "Query não informada"}), 400

        # Bloqueio de empilhamento de comandos (query stacking)
        if ";" in query.rstrip(";"):
            return jsonify({"erro": "Múltiplos comandos SQL não são permitidos"}), 400

        # Permitir estritamente consultas SELECT de leitura
        normalized = query.upper()
        if not normalized.startswith("SELECT"):
            return jsonify({
                "erro": "Execução restrita: Apenas consultas de leitura (SELECT) são permitidas por motivos de segurança. Para mutações, utilize os endpoints administrativos específicos."
            }), 403

        # Blacklist de segurança adicional para subconsultas/funções perigosas
        forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA", "EXEC"]
        tokens = [t.strip("(),;") for t in normalized.split()]
        if any(token in tokens for token in forbidden_keywords if token != "SELECT"):
            return jsonify({"erro": "Comando proibido detectado na consulta"}), 403

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return jsonify({"dados": [dict(r) for r in rows], "sucesso": True}), 200
        except Exception as e:
            return jsonify({"erro": "Erro na execução da consulta de leitura"}), 400
```

---

## 6. Criptografia Segura de Senhas (Substituição de MD5 / Plaintext)
**Problema**: Senhas de usuários salvas em texto puro ou hasheadas com algoritmos criptograficamente quebrados (MD5, SHA-1, ou Base64 caseiro).  
**Solução**: Empregar algoritmos de derivação de chave com salt automático (PBKDF2, BCrypt ou Argon2).

### Exemplo (Python: Werkzeug / Node.js: Crypto/Bcrypt)
#### ❌ Antes (MD5 ou Texto Puro)
```python
# models/user.py
def set_password(self, pwd):
    self.password = hashlib.md5(pwd.encode()).hexdigest() # Vulnerável a colisões e rainbow tables
```

#### ✅ Depois (PBKDF2 com Salt)
```python
# models/user.py
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    def set_password(self, pwd):
        self.password = generate_password_hash(pwd, method="pbkdf2:sha256")

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
```

---

## 7. Eliminação do Problema de Consultas N+1 (Resource Exhaustion)
**Problema**: Buscar uma coleção principal e, dentro de uma iteração no código, executar uma consulta adicional no banco para cada elemento retornado.  
**Solução**: Utilizar `JOIN` relacional, cláusula `IN`, ou agregação via `GROUP BY` para trazer todos os dados necessários em uma única requisição ao banco.

### Exemplo (Python / SQL)
#### ❌ Antes (Loop executando N queries individuais)
```python
def obter_resumo_usuarios():
    usuarios = db.session.query(User).all()
    resumo = []
    for u in usuarios:
        # N queries executadas individualmente dentro do loop
        total_tarefas = db.session.query(Task).filter_by(user_id=u.id).count()
        resumo.append({"user": u.name, "total_tarefas": total_tarefas})
    return resumo
```

#### ✅ Depois (Consulta Única Agregada com GROUP BY / JOIN)
```python
def obter_resumo_usuarios():
    # 1 única query agregada
    resultados = db.session.query(
        User.id,
        User.name,
        db.func.count(Task.id).label("total_tarefas")
    ).outerjoin(Task, User.id == Task.user_id)\
     .group_by(User.id, User.name).all()

    return [{"user": r.name, "total_tarefas": r.total_tarefas} for r in resultados]
```

---

## 8. Tratamento Centralizado de Exceções e Erros Globais
**Problema**: Blocos `try/except` ou `try/catch` dispersos por todos os arquivos retornando formatos de resposta inconsistentes ou engolindo erros silenciosamente.  
**Solução**: Implementar manipulador de erros global (error handling middleware) padronizando respostas em formato JSON com código de status HTTP correto.

### Exemplo (Flask & Express)
#### ❌ Antes (Blocos dispersos com inconsistência de status)
```python
@app.route("/item/<id>")
def get_item(id):
    try:
        return db.find(id)
    except:
        return "erro", 200 # Erro com status HTTP 200 (sucesso falso)
```

#### ✅ Depois (Middleware / Error Handler Centralizado)
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado", "status": 404}), 404

    @app.errorhandler(Exception)
    def internal_error(e):
        app.logger.error(f"Erro não tratado: {str(e)}")
        return jsonify({"erro": "Erro interno do servidor", "status": 500}), 500
```

---

## 9. Eliminação de Estado Global Mutável
**Problema**: Uso de variáveis no escopo do módulo para armazenar dados em cache, acumuladores ou sessões, gerando race conditions em ambientes multi-thread/multi-processo.  
**Solução**: Encapsular o estado em repositórios, serviços instanciados ou componentes de cache explícitos.

### Exemplo (Node.js)
#### ❌ Antes (Variáveis Globais Mutáveis no Módulo)
```javascript
// utils.js
let globalCache = {};
let totalRevenue = 0;

function recordSale(amount) {
    totalRevenue += amount; // Estado global mutável imprevisível
}
```

#### ✅ Depois (Serviço de Domínio com Persistência em Banco)
```javascript
// services/MetricsService.js
class MetricsService {
    static async recordSale(db, amount) {
        // Persistido confiavelmente no banco de dados
        await db.run("UPDATE metrics SET total_revenue = total_revenue + ? WHERE id = 1", [amount]);
    }

    static async getRevenue(db) {
        const row = await db.get("SELECT total_revenue FROM metrics WHERE id = 1");
        return row ? row.total_revenue : 0;
    }
}
```

---

## 10. Substituição de Magic Numbers e Strings por Constantes e Enums
**Problema**: Strings e números mágicos literais espalhados por condicionais (`if status == 1`, `if category in ["eletronicos", "livros"]`), dificultando refatorações e gerando bugs por digitação.  
**Solução**: Definir enumerações ou dicionários de constantes em módulo de domínio.

### Exemplo (Python)
#### ❌ Antes (Valores Literais Espalhados)
```python
def validar_produto(dados):
    if dados["categoria"] not in ["eletronicos", "roupas", "alimentos", "livros"]:
        return False
```

#### ✅ Depois (Constantes no Model de Domínio)
```python
# models/produto_model.py
class CategoriaProduto:
    ELETRONICOS = "eletronicos"
    ROUPAS = "roupas"
    ALIMENTOS = "alimentos"
    LIVROS = "livros"

    TODAS = [ELETRONICOS, ROUPAS, ALIMENTOS, LIVROS]

def validar_produto(dados):
    return dados.get("categoria") in CategoriaProduto.TODAS

---

## 11. Prevenção de SQL Injection em Buscas Dinâmicas com Filtros Opcionais
**Problema**: Funções de busca que constroem queries SQL dinamicamente concatenando filtros opcionais passados pelo usuário via query string ou payload (`request.args.get`, `req.query`). Mesmo que cada filtro individualmente pareça inofensivo, a concatenação direta abre vetores de injeção clássicos e de segundo grau.  
**Solução**: Construir a query com placeholders `?` para cada filtro ativo e acumular os valores em uma lista de parâmetros, passando ambos ao `cursor.execute()`.

### Exemplo (Python / SQLite)
#### ❌ Antes (Filtros Opcionais Concatenados — Vulnerável)
```python
# models.py
def buscar_produtos(termo, categoria=None, preco_min=None, preco_max=None):
    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM produtos WHERE 1=1"
    if termo:
        query += " AND (nome LIKE '%" + termo + "%' OR descricao LIKE '%" + termo + "%')"  # INJEÇÃO
    if categoria:
        query += " AND categoria = '" + categoria + "'"  # INJEÇÃO
    if preco_min:
        query += " AND preco >= " + str(preco_min)
    if preco_max:
        query += " AND preco <= " + str(preco_max)

    cursor.execute(query)  # ← executa query construída por concatenação de input do usuário
    return [dict(row) for row in cursor.fetchall()]
```

#### ✅ Depois (Parametrização Completa com Lista de Filtros)
```python
# src/models/produto_model.py
class ProdutoModel:
    @staticmethod
    def buscar(termo: str = "", categoria: str = None,
               preco_min: float = None, preco_max: float = None) -> list:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * FROM produtos WHERE 1=1"
        params = []

        if termo:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            params.extend([f"%{termo}%", f"%{termo}%"])
        if categoria:
            query += " AND categoria = ?"
            params.append(categoria)
        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)
        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)

        cursor.execute(query, params)  # ← parâmetros passados separadamente, nunca interpolados
        return [dict(row) for row in cursor.fetchall()]
```

---

## 12. Segregação de Rotas por Domínio (Violação de SRP em Blueprints)
**Problema**: Endpoints CRUD de uma entidade (ex: `/categories`) implementados dentro do módulo de rotas de outro domínio (ex: `report_routes.py`), criando acoplamento indevido entre domínios e violando o Princípio da Responsabilidade Única (SRP).  
**Solução**: Criar um Blueprint dedicado por entidade de domínio, registrando cada um individualmente no `app.py`.

### Exemplo (Python / Flask)
#### ❌ Antes (CRUD de Categorias misturado em report_routes.py)
```python
# routes/report_routes.py  ← arquivo de relatórios contendo CRUD de outra entidade
report_bp = Blueprint('report', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    ...  # lógica de relatório

# ERRADO: endpoints de categories dentro do arquivo de reports
@report_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

@report_bp.route('/categories', methods=['POST'])
def create_category():
    ...

@report_bp.route('/categories/<int:cat_id>', methods=['PUT', 'DELETE'])
def manage_category(cat_id):
    ...
```

#### ✅ Depois (Blueprint Dedicado por Domínio)
```python
# routes/report_routes.py  ← apenas relatórios
report_bp = Blueprint('report', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    from services.report_service import ReportService
    return jsonify(ReportService.get_summary()), 200

# routes/category_routes.py  ← domínio exclusivo de categorias
from flask import Blueprint, request, jsonify
from models.category import Category
from database import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = [c.to_dict() for c in categories]
    return jsonify(result), 200

@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Nome é obrigatório'}), 400
    category = Category(name=data['name'],
                        description=data.get('description', ''),
                        color=data.get('color', '#000000'))
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    data = request.get_json()
    for field in ('name', 'description', 'color'):
        if field in data:
            setattr(cat, field, data[field])
    db.session.commit()
    return jsonify(cat.to_dict()), 200

@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'Categoria deletada'}), 200

# app.py  ← ambos os blueprints registrados separadamente
from routes.report_routes import report_bp
from routes.category_routes import category_bp

app.register_blueprint(report_bp)
app.register_blueprint(category_bp)
```

## 13. [LOW] Uso de APIs Obsoletas (Deprecated)

**Problema:** Uso de bibliotecas, funções ou construtores que foram descontinuados (deprecated).
**Solução:** Substituir pelo equivalente moderno recomendado.

### Exemplo (Node.js / Crypto)

#### ❌ Antes (API Obsoleta)
```javascript
const crypto = require('crypto');

function encrypt(text, key) {
    // createCipher está deprecated porque não usa um Vetor de Inicialização (IV)
    const cipher = crypto.createCipher('aes-256-cbc', key); 
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
}
```

#### ✅ Depois (Equivalente Moderno)
```javascript
const crypto = require('crypto');

function encrypt(text, key) {
    // createCipheriv é o equivalente moderno e requer um IV para segurança
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return iv.toString('hex') + ':' + encrypted;
}
```
