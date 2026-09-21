# Conhecimento: Análise de Projeto

Heurísticas avançadas para detecção de stack, mapeamento de arquitetura e localização precisa de vulnerabilidades.

## 1. Detecção de Stack (Multi-Linguagem)

### Linguagens & Frameworks
- **Python**: `requirements.txt`, `Pipfile`, `pyproject.toml`. Frameworks: Flask, Django, FastAPI.
- **Node.js (JS/TS)**: `package.json`. Frameworks: Express, NestJS, Fastify, AdonisJS. (TS se houver `tsconfig.json`).
- **Go**: `go.mod`. Frameworks: Gin, Echo, Fiber.
- **Java**: `pom.xml` (Maven) ou `build.gradle` (Gradle). Frameworks: Spring Boot, Quarkus.
- **C#**: `.csproj`, `sln`. Frameworks: ASP.NET Core.
- **C++**: `CMakeLists.txt`, `Makefile`. Frameworks: Drogon, Qt.
- **PHP**: `composer.json`. Frameworks: Laravel, Symfony.

### Bancos de Dados & Conectores
- **SQL (Relacional)**:
  - **SQLite**: `sqlite3`, `loja.db`, `:memory:`.
  - **PostgreSQL**: `psycopg2`, `pg`, `npgsql`, `gorm`.
  - **MySQL/MariaDB**: `mysql-connector`, `mysql2`, `Pomelo`.
  - **SQL Server**: `pyodbc`, `mssql`, `tedious`.
  - **Oracle**: `cx_Oracle`, `node-oracledb`.
- **NoSQL & Cache**:
  - **MongoDB**: `pymongo`, `mongodb`, `mongoose`.
  - **Redis**: `redis-py`, `ioredis`, `StackExchange.Redis`.
  - **Cassandra/ScyllaDB**: `cassandra-driver`.

## 2. Mapeamento de Arquitetura
- **Monolítico (Básico)**: Todo o código na raiz ou em poucos arquivos.
- **Camadas (Layered)**: Pastas `models`, `views`, `controllers` presentes.
- **Spaghetti**: Estrutura de pastas presente, mas com lógica de negócio e SQL misturados em rotas.
- **Hexagonal/Clean**: Presença de `domain`, `use_cases`, `adapters`, `entities`.

## 3. Identificação de Domínio
- Analisar nomes de tabelas, endpoints e modelos (ex: `order`, `cart`, `payment` -> E-commerce; `task`, `todo`, `deadline` -> Gestão de Tarefas).

## 4. Diretrizes de Localização Precisa de Findings

A linha reportada em cada finding deve identificar inequivocamente a instrução problemática — não linhas adjacentes de setup, retorno ou leitura de resultado. As regras abaixo se aplicam a todos os tipos de achado:

| Tipo de Finding | Linha a reportar |
|---|---|
| **SQL Injection (query direta)** | A linha do `cursor.execute(...)`, `db.run(...)` ou `db.query(...)` que recebe input do usuário |
| **SQL Injection (filtros opcionais)** | A linha onde a concatenação perigosa ocorre (ex: `query += " AND nome LIKE '%" + termo + "%'"`) |
| **Credenciais hardcoded** | A linha da atribuição literal (`SECRET_KEY = "..."`, `const API_KEY = "sk_live_..."`) |
| **Hash inseguro** | A linha da chamada ao algoritmo (`hashlib.md5(...)`, `crypto.createHash('sha1')`, `badCrypto(...)`) |
| **Senha em `to_dict()`** | A linha `'password': self.password` dentro do método de serialização |
| **Estado global mutável** | A linha da declaração da variável global (`let globalCache = {}`, `let totalRevenue = 0`) |
| **N+1** | A linha da query disparada dentro do loop (ex: `cursor.execute(...)` indentado sob `for`) |
| **Fat Route** | O intervalo de linhas do handler completo (ex: `def summary_report():` linha X até `return jsonify(...), 200` linha Y) |
| **SRP / Handler Misto** | O intervalo de linhas das rotas do domínio incorreto dentro do arquivo |

> **Cobertura de SQL Injection**: verificar o arquivo inteiro, não apenas as chamadas `cursor.execute` evidentes. Funções de busca que iniciam uma query base (`SELECT * FROM tabela WHERE 1=1`) e acrescentam filtros condicionalmente via concatenação com dados de `request.args`, `req.query` ou `req.body` são igualmente críticas.
