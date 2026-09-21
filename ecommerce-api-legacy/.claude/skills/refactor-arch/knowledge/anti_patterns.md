# Conhecimento: Catálogo de Anti-Padrões (Universal)

Catálogo exaustivo de anti-padrões arquiteturais, de segurança e de qualidade de código, aplicáveis a múltiplas stacks tecnológicas. A Skill deve utilizar este catálogo para identificar **no mínimo 5 findings** por projeto na Fase 2 de Auditoria, com severidades distribuídas (CRITICAL, HIGH, MEDIUM, LOW).

---

## 1. Segurança & Integridade de Dados

### [CRITICAL] Vulnerabilidades de Injeção de SQL / NoSQL
- **Sinais de Detecção**:
  - Concatenação, interpolação de strings (`f"..."`, `+`) ou formatação com dados de entrada de usuário em queries: ex. `cursor.execute("SELECT * FROM users WHERE id = " + user_id)` ou `query = f"SELECT * FROM produtos WHERE nome = '{nome}'"`.
  - Funções de busca que iniciam uma query base e acrescentam filtros condicionalmente a partir de parâmetros da requisição (`request.args.get`, `req.query`, `req.body`) usando `+=` ou concatenação: ex. `query += " AND nome LIKE '%" + termo + "%'"`. Este padrão tem o mesmo nível de criticidade das injeções diretas e ocorre com frequência em funcionalidades de pesquisa e filtragem.
- **Impacto no Negócio**: Risco de extração total de dados (data breach), evasão de autenticação ou destruição da base de dados (OWASP A03).
- **Recomendação**: Utilizar exclusivamente consultas parametrizadas com placeholders (`?`, `$1`, `:param`). Para filtros opcionais, acumular valores em uma lista `params` e passar ao `cursor.execute(query, params)` — nunca interpolar diretamente na string da query.

### [CRITICAL] Endpoint Administrativo de SQL Livre / Execução Arbitrária de Queries
- **Sinais de Detecção**: Endpoints HTTP (como `/admin/query` ou `/api/execute-sql`) que aceitam strings SQL brutas no corpo da requisição e as executam diretamente com `cursor.execute(sql)` ou `db.query(sql)`, inclusive quando há tentativas de validação posteriores à execução.
- **Exemplos**: Receber `dados.get("sql")` e executar antes de qualquer validação, ou checar `startswith("SELECT")` após o `cursor.execute`.
- **Impacto no Negócio**: Backdoor de execução arbitrária de comandos SQL no banco. Permite exclusão instantânea de tabelas (`DROP TABLE`), inserção de backdoors e bypass de todas as regras de negócio.
- **Recomendação**: Substituir por endpoints administrativos especializados e parametrizados (ex: `/admin/reset-database`). Se mantido para inspeção de leitura, validar e restringir categoricamente *antes* da execução: allowlist de `SELECT`, rejeitar encadeamento de múltiplos comandos (`;`), e bloquear palavras-chave destrutivas via tokenização.

### [CRITICAL] Exposição de Credenciais e Segredos Hardcoded
- **Sinais de Detecção**: Chaves de API (`sk_live_...`, `pk_live_...`), segredos de criptografia (`SECRET_KEY`), senhas de banco ou tokens de pagamento gravados como literais de string no código-fonte ou expostos em respostas de endpoints internos (ex: endpoint `/health` retornando `secret_key`).
- **Exemplos**: `app.config['SECRET_KEY'] = 'minha-chave-super-secreta-123'`, `const DB_PASS = "admin123"`, `paymentGatewayKey: "pk_live_1234567890abcdef"`.
- **Impacto no Negócio**: Comprometimento direto da infraestrutura, facilitação de ataques de personificação e violação severa de normas de conformidade (LGPD, GDPR, PCI-DSS).
- **Recomendação**: Mover todas as credenciais para variáveis de ambiente via módulo de configuração centralizado (`config/settings.py` ou `config/index.js`). Nunca incluir segredos em payloads de resposta HTTP.

### [HIGH] Autenticação Quebrada & Algoritmos Criptográficos Obsoletos
- **Sinais de Detecção**: Armazenamento de senhas em texto puro; funções de cifra customizadas reversíveis (ex: loops de Base64 concatenado); uso de algoritmos criptograficamente obsoletos e vulneráveis a colisões como `hashlib.md5()`, `hashlib.sha1()` ou `crypto.createHash('sha1')`.
- **Exemplos**: `hashlib.md5(pwd.encode()).hexdigest()` para armazenar senha; comparação de senha na query SQL sem hash.
- **Impacto no Negócio**: Se a base de dados for acessada, todas as credenciais de usuários e administradores são imediatamente expostas ou quebradas com rainbow tables.
- **Recomendação**: Substituir por funções robustas de derivação de chave com salt único por usuário (PBKDF2 via `werkzeug.security`, `bcrypt` ou `argon2`). Para Node.js, usar `crypto.createHash('sha256')` com `randomBytes(16)` para o salt, ou biblioteca `bcrypt`.

### [MEDIUM] Vazamento de Dados Sensíveis na Serialização
- **Sinais de Detecção**: Métodos de serialização (`to_dict()`, `toJSON()`) que incluem campos confidenciais (`password`, `hash`, `auth_token`, `secret`) no payload de resposta de APIs públicas ou semi-públicas.
- **Exemplos**: `return {'id': self.id, 'name': self.name, 'password': self.password}` em models de usuário expostos em `GET /users`.
- **Impacto no Negócio**: Exposição acidental de hashes ou senhas em listagens de usuários na API, facilitando ataques offline de força bruta.
- **Recomendação**: Omitir campos sensíveis na serialização padrão de entidades ou criar DTOs/ViewModels específicos de saída.

### [MEDIUM] Falta de Integridade Referencial em Exclusões
- **Sinais de Detecção**: Operações de deleção de entidades pai (ex: usuários) sem remoção de registros dependentes (ex: pedidos, matrículas), sem uso de transações ou sem `ON DELETE CASCADE` nas foreign keys.
- **Exemplos**: `DELETE FROM users WHERE id = ?` deixando registros filhos órfãos. Código que comenta explicitamente a inconsistência ("usuário deletado, mas matrículas ficaram sujas").
- **Impacto no Negócio**: Inconsistência de dados relacional, relatórios financeiros incorretos e erros de chave estrangeira futuros.
- **Recomendação**: Implementar exclusão em cascata transacional (`BEGIN TRANSACTION` + deleção de dependentes + deleção da entidade pai) na camada de Model.

---

## 2. Design Arquitetural & Princípios SOLID

### [CRITICAL] God Object / Componente Monolítico (Violação de SRP)
- **Sinais de Detecção**: Arquivo ou classe única que centraliza múltiplas responsabilidades não correlacionadas: rotas HTTP, persistência em banco, regras de negócio e formatação de resposta. Tipicamente mais de 200 linhas em um único arquivo com funções de domínios distintos.
- **Exemplos**: `models.py` com 300+ linhas contendo todas as tabelas e regras, ou `AppManager.js` gerenciando rotas, banco e pagamentos.
- **Impacto no Negócio**: Sistema de altíssimo risco de manutenção; qualquer alteração pontual pode quebrar funcionalidades não relacionadas. Impossível escrever testes unitários isolados.
- **Recomendação**: Decompor o monólito seguindo o padrão MVC (Models, Controllers e Rotas separados por domínio), conforme `knowledge/mvc_guidelines.md`.

### [HIGH] Vazamento de Lógica de Negócio e Persistência na Camada de Transporte
- **Sinais de Detecção**: Funções de rota ou controllers com dezenas de linhas de regras de cálculo, controle de fluxo complexo, ou instanciando conexões e cursores de banco de dados diretamente (`db.cursor()`, `cursor.execute()`).
- **Exemplos**: Handler de relatório contendo queries ORM diretas, ou um Controller (como `AdminController` ou `HealthController`) executando consultas de contagem ou remoção diretamente no banco via `get_db()`.
- **Impacto no Negócio**: Quebra da separação de preocupações (MVC), impossibilidade de reutilizar queries e lógica de negócio em outros pontos da aplicação (jobs, CLI) e dificuldade extrema de testabilidade unitária (pois obriga o mock da conexão HTTP e do Banco de Dados simultaneamente).
- **Recomendação**: Extrair toda a lógica analítica e de acesso a dados para a Camada de Serviço (`ReportService`) ou para a Camada de Model (`AdminModel`, `HealthModel`). Os handlers e controllers devem ter a responsabilidade estrita de receber a requisição, chamar o Model/Service e devolver a resposta HTTP.

### [LOW] Violação de SRP nas Rotas / Handlers Mistos
- **Sinais de Detecção**: Arquivo de rotas nomeado para um domínio (ex: `report_routes.py`) contendo endpoints CRUD de outro domínio não relacionado (ex: categorias, usuários).
- **Impacto no Negócio**: Dificuldade de rastreamento de endpoints, aumento do acoplamento entre domínios e confusão na evolução da API.
- **Recomendação**: Separar rotas em Blueprints/módulos dedicados por entidade de domínio (ex: `category_routes.py`), registrando cada Blueprint individualmente na aplicação.

---

## 3. Performance & Qualidade de Código

### [MEDIUM] Consulta N+1 & Exaustão de Recursos
- **Sinais de Detecção**: Execução de queries individuais dentro de loops de repetição para buscar dados de itens relacionados a cada registro principal. Presença de múltiplos `cursor.execute`, `Task.query.filter_by`, `db.get` etc. aninhados em `for` ou `foreach`.
- **Exemplos**: Para cada pedido, uma nova query para buscar os itens; para cada usuário, uma nova query ORM para contar tarefas — resultando em `1 + N + (N×M)` queries ao banco.
- **Impacto no Negócio**: Lentidão exponencial conforme o volume de dados cresce, gerando sobrecarga desnecessária no banco e custos extras de infraestrutura.
- **Recomendação**: Substituir por consultas com `JOIN`, cláusula `IN`, ou agregação via `GROUP BY` em query única. Para ORM (SQLAlchemy), usar `db.session.query(...).join(...).group_by(...)`.

### [LOW] Estado Global Mutável
- **Sinais de Detecção**: Variáveis mutáveis declaradas no escopo global ou de módulo (dicionários de cache, contadores acumuladores de receita) alteradas por múltiplas requisições concorrentes sem sincronização.
- **Exemplos**: `let globalCache = {}; let totalRevenue = 0;` em arquivos utilitários compartilhados entre requests.
- **Impacto no Negócio**: Race conditions, perda de sincronia entre instâncias e comportamento imprevisível da aplicação sob carga.
- **Recomendação**: Eliminar estado global mutável; persistir informações de negócio no banco de dados (ex: `SUM(price)` via query) e usar cache thread-safe ou distribuído se necessário.

### [LOW] Obsessão por Primitivos & Magic Strings / Numbers
- **Sinais de Detecção**: Strings ou inteiros soltos no código representando categorias, papéis (`role`) ou status sem o uso de constantes ou enums — especialmente quando a mesma lista aparece duplicada em múltiplas funções.
- **Exemplos**: `if categoria not in ["eletronicos", "roupas", "alimentos", "livros"]` chumbado em funções de controller.
- **Impacto no Negócio**: Propagação de erros de digitação, duplicação de listas e alto custo para inclusão de novos valores de domínio.
- **Recomendação**: Definir classes de constantes ou Enums no Model correspondente (ex: `class CategoriaProduto: TODAS = [...]`).

### [LOW] Uso de APIs Obsoletas (Deprecated)
- **Sinais de Detecção**: Uso de funções, bibliotecas ou métodos nativos que foram oficialmente marcados como obsoletos (deprecated) na documentação da linguagem ou framework.
- **Exemplos**: Em Node.js, usar `crypto.createCipher` (deprecated) em vez de `crypto.createCipheriv`. Em Python, usar `md5` sem propósitos criptográficos adequados.
- **Impacto no Negócio**: Vulnerabilidades de segurança não corrigidas na API antiga, e quebra total da funcionalidade quando a linguagem remover a API em atualizações futuras.
- **Recomendação**: Identificar o uso de APIs obsoletas e substituir pelo equivalente moderno recomendado pela documentação (ex: migrar de `createCipher` para `createCipheriv` com Vetor de Inicialização).
