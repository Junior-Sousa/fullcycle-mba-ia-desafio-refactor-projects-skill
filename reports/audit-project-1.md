# AUDITORIA ARQUITETURAL & AVALIAÇÃO TÉCNICA
**Projeto**: code-smells-project  
**Arquiteto**: Especialista Refactor-Arch  
**Data da Avaliação**: 2026-09-21  
**Visão Geral da Stack**: Python 3.x | Flask 3.1.1 | SQLite 3 (loja.db)  

## 1. Resumo Executivo
O projeto `code-smells-project` consiste em uma API de E-commerce monolítica estruturada em apenas 4 arquivos na raiz (`app.py`, `database.py`, `models.py`, `controllers.py`), totalizando aproximadamente 784 linhas de código. A aplicação apresenta severo débito técnico, ausência de separação por domínios de negócio e violações críticas de segurança — destacando-se múltiplas vulnerabilidades de SQL Injection (inclusive em endpoints de busca com concatenação dinâmica de filtros), um endpoint administrativo com backdoor para execução de SQL livre, armazenamento e comparação de senhas em texto puro, e vazamento de credenciais e segredos em endpoints públicos (`SECRET_KEY` exposta em `/health`). Em termos de performance e manutenibilidade, foram identificadas consultas com padrão N+1 aninhado, acoplamento de estado global na conexão do banco e violações sistemáticas dos princípios SOLID e da arquitetura MVC.

**Tabela de Métricas**:
| Severidade | Contagem | Nível de Impacto |
|---|---|---|
| **CRITICAL** | 5 | Alto Risco / Ação Imediata |
| **HIGH** | 2 | Débito Estrutural / Risco de Segurança |
| **MEDIUM** | 2 | Performance / Manutenibilidade |
| **LOW** | 2 | Code Smell / Boas Práticas |

---

## 2. Achados Detalhados

### [CRITICAL] SQL Injection em Consultas Diretas de CRUD
- **Localização**: `models.py:28`, `models.py:48-50`, `models.py:57-61`, `models.py:68`, `models.py:92`, `models.py:109-111`, `models.py:127-129`, `models.py:149-151`, `models.py:157-161`, `models.py:164-166`, `models.py:279-281`
- **Padrão**: Vulnerabilidades de Injeção de SQL / NoSQL
- **Análise**: O código realiza interpolação e concatenação direta de strings com parâmetros recebidos do usuário (`str(id)`, `nome`, `email`, `senha`, `novo_status`) em múltiplos comandos `cursor.execute(...)` para `SELECT`, `INSERT`, `UPDATE` e `DELETE`.
- **Impacto de Negócio**: Permite ataque de SQL Injection clássico, possibilitando que atacantes extraiam todo o banco de dados, excluam tabelas ou alterem privilégios de acesso sem autenticação válida.
- **Recomendação Arquitetural**: Eliminar toda e qualquer concatenação de strings em instruções SQL, adotando exclusivamente consultas parametrizadas com placeholders `?` suportados pelo driver SQLite.

### [CRITICAL] SQL Injection em Buscas Dinâmicas com Filtros Opcionais
- **Localização**: `models.py:291-298`
- **Padrão**: Vulnerabilidades de Injeção de SQL / NoSQL (Busca Dinâmica com Concatenação)
- **Análise**: Na função `buscar_produtos()`, os parâmetros opcionais `termo`, `categoria`, `preco_min` e `preco_max` recebidos via query parameters (`request.args`) são concatenados diretamente com `+=` na cláusula `WHERE 1=1`, abrindo vetor de injeção direta no endpoint de pesquisa pública (`/produtos/busca`).
- **Impacto de Negócio**: Permite exploração de injeção SQL através do endpoint público de busca, viabilizando exfiltração de dados e bypass das restrições da API.
- **Recomendação Arquitetural**: Construir a consulta dinâmica utilizando placeholders `?` para cada filtro ativo e repassar os valores através de uma lista de parâmetros `params` ao `cursor.execute(query, params)`.

### [CRITICAL] Endpoint Administrativo de Execução Arbitrária de SQL Livre
- **Localização**: `app.py:69`
- **Padrão**: Endpoint Administrativo de SQL Livre / Execução Arbitrária de Queries
- **Análise**: A rota `POST /admin/query` recebe uma string SQL bruta enviada no payload JSON (`dados.get("sql")`) e a executa diretamente no banco com `cursor.execute(query)` sem validação de permissões, token de segurança ou sanitização de comandos destrutivos.
- **Impacto de Negócio**: Funciona como um backdoor de execução remota de comandos SQL, permitindo `DROP TABLE`, manipulação indiscriminada de saldos e criação de administradores ilícitos por qualquer cliente HTTP.
- **Recomendação Arquitetural**: Remover ou isolar o endpoint sob camadas estritas de controle: bloquear instruções destrutivas (DDL/DML), rejeitar query stacking (bloqueio do caractere `;`), permitir apenas consultas `SELECT` de leitura estrita e transferir operações legítimas de manutenção para endpoints administrativos específicos (como `/admin/reset-db`).

### [CRITICAL] Exposição de Credenciais Hardcoded e Segredos na API
- **Localização**: `app.py:7` e `controllers.py:289`
- **Padrão**: Exposição de Credenciais e Segredos Hardcoded
- **Análise**: A chave secreta da aplicação (`SECRET_KEY`) está definida como literal de string `"minha-chave-super-secreta-123"` no código-fonte em `app.py:7` e, adicionalmente, é exposta publicamente na resposta do endpoint de monitoramento `GET /health` (`controllers.py:289`), junto com a flag `debug: True`.
- **Impacto de Negócio**: Violação direta de normas de conformidade (LGPD, PCI-DSS). Permite a forja de sessões de autenticação, falsificação de cookies criptografados e reconhecimento detalhado da infraestrutura interna por terceiros maliciosos.
- **Recomendação Arquitetural**: Mover a `SECRET_KEY` para variáveis de ambiente carregadas através de um módulo `src/config/settings.py` e sanitizar o payload do endpoint `/health`, retornando apenas métricas operacionais desprovidas de segredos.

### [CRITICAL] God Object / Falta de Separação de Domínios em models.py
- **Localização**: `models.py:1-315`
- **Padrão**: God Object / Componente Monolítico (Violação de SRP)
- **Análise**: O arquivo `models.py` concentra mais de 300 linhas de código contendo o acesso a dados, lógica de negócio, regras de desconto, validação de estoque e cálculos financeiros de quatro domínios não correlacionados: produtos, usuários, pedidos e relatórios de vendas.
- **Impacto de Negócio**: Altíssimo custo de manutenção, impossibilidade de criar testes unitários isolados e elevado risco de efeitos colaterais onde alterações em um domínio quebram funcionalidades de outro.
- **Recomendação Arquitetural**: Decompor o monólito seguindo o padrão MVC em modelos específicos por entidade (`ProdutoModel`, `UsuarioModel`, `PedidoModel`, `ItemPedidoModel`) dentro de `src/models/`, e extrair a lógica de cálculo analítico para `src/services/report_service.py`.

### [HIGH] Senhas Armazenadas e Comparadas em Texto Puro
- **Localização**: `database.py:76-83` e `models.py:109-112`
- **Padrão**: Autenticação Quebrada & Algoritmos Criptográficos Obsoletos
- **Análise**: O seed do banco de dados insere senhas em texto puro (`admin123`, `123456`, `senha123`), e a função `login_usuario()` em `models.py` compara diretamente a senha recebida em texto plano com a coluna no banco (`WHERE email = ... AND senha = ...`).
- **Impacto de Negócio**: Comprometimento absoluto das contas de usuários e administradores em caso de vazamento da base de dados, expondo a organização a severas sanções regulatórias.
- **Recomendação Arquitetural**: Implementar hashing criptográfico com derivação de chave e salt via `werkzeug.security.generate_password_hash` no cadastro/seed e validação através de `check_password_hash` no fluxo de autenticação.

### [HIGH] Vazamento de Acesso a Banco e Persistência na Camada de Transporte
- **Localização**: `controllers.py:266-274` e `app.py:47-79`
- **Padrão**: Vazamento de Lógica de Negócio e Persistência na Camada de Transporte
- **Análise**: O controller `health_check()` executa queries diretas de contagem instanciando conexões e cursores, e o arquivo principal `app.py` implementa rotas administrativas contendo instruções SQL embutidas em vez de delegar as operações para a camada de Model/Service.
- **Impacto de Negócio**: Violação da separação de preocupações (SoC), impossibilitando a reutilização de regras em outros contextos e exigindo mocking de conexões de banco ao testar rotas HTTP.
- **Recomendação Arquitetural**: Delegar todas as interações com o banco de dados exclusivamente para a camada de Model/Repository e manter controllers finos e focados na orquestração HTTP.

### [MEDIUM] Consulta N+1 na Listagem e Detalhamento de Pedidos
- **Localização**: `models.py:187-193` e `models.py:219-225`
- **Padrão**: Consulta N+1 & Exaustão de Recursos
- **Análise**: Nas funções `get_pedidos_usuario()` e `get_todos_pedidos()`, o código itera sobre cada pedido retornado e dispara uma query adicional para buscar seus itens (`cursor2`), e dentro de cada item dispara uma terceira query para buscar o nome do produto correspondente (`cursor3`), gerando um padrão de exaustão de consultas `1 + N + (N * M)`.
- **Impacto de Negócio**: Degradação severa e exponencial de performance da API conforme a base de dados cresce, elevando a latência e o consumo de I/O no banco.
- **Recomendação Arquitetural**: Reestruturar a recuperação de dados através de consultas relacionais consolidadas com `JOIN` entre `pedidos`, `itens_pedido` e `produtos`, agrupando os itens na memória.

### [MEDIUM] Vazamento de Dados Sensíveis na Serialização de Usuários
- **Localização**: `models.py:83` e `models.py:99`
- **Padrão**: Vazamento de Dados Sensíveis na Serialização
- **Análise**: As rotas de listagem (`GET /usuarios`) e busca por identificador (`GET /usuarios/<id>`) retornam as senhas dos usuários cadastradas no banco no corpo da resposta JSON.
- **Impacto de Negócio**: Exposição indevida das credenciais de todos os usuários a qualquer cliente da API pública.
- **Recomendação Arquitetural**: Omitir o campo `senha` na serialização padrão das entidades de usuário retornadas pela API.

### [LOW] Estado Global Mutável na Gestão de Conexões do Banco
- **Localização**: `database.py:4` e `database.py:8-10`
- **Padrão**: Estado Global Mutável
- **Análise**: O arquivo `database.py` armazena a instância da conexão em uma variável global mutável `db_connection` compartilhada entre todas as threads (`check_same_thread=False`), sem ciclo de vida delimitado por requisição.
- **Impacto de Negócio**: Risco de race conditions, bloqueios de escrita concorrente no SQLite e comportamentos inconsistentes sob cargas elevadas.
- **Recomendação Arquitetural**: Gerenciar o ciclo de vida da conexão por requisição através do contexto da aplicação Flask (`flask.g`) ou através de um context manager seguro.

### [LOW] Obsessão por Primitivos e Magic Strings em Categorias e Status
- **Localização**: `controllers.py:52-54`, `controllers.py:242`, `models.py:247-254`
- **Padrão**: Obsessão por Primitivos & Magic Strings / Numbers
- **Análise**: As listas de categorias válidas (`["informatica", "moveis", ...]`) e status de pedidos (`["pendente", "aprovado", ...]`) encontram-se literais e duplicadas em diferentes funções de controllers e models.
- **Impacto de Negócio**: Propensão a falhas de consistência e alto custo de manutenção ao adicionar ou renomear categorias e status de negócio.
- **Recomendação Arquitetural**: Centralizar as listas de domínios permitidos em constantes ou Enums de domínio nos respectivos models.

---

## 3. Arquitetura Alvo Proposta
- **Padrão**: Model-View-Controller (MVC) com Camada de Serviço e Configuração Centralizada
- **Plano de Refatoração**:
  1. **Estrutura de Pastas Padronizada**:
     - `src/config/`: `settings.py` (variáveis de ambiente, debug, chaves secretas).
     - `src/database/`: `connection.py` (gestão segura de conexão SQLite e migrações/seed).
     - `src/models/`: `produto_model.py`, `usuario_model.py`, `pedido_model.py`, `item_pedido_model.py`.
     - `src/services/`: `report_service.py` (cálculo de descontos e métricas de vendas) e `auth_service.py`.
     - `src/controllers/`: `produto_controller.py`, `usuario_controller.py`, `pedido_controller.py`, `report_controller.py`, `admin_controller.py`.
     - `src/routes/`: Blueprints dedicados por domínio registrados no `app.py`.
     - `src/middlewares/`: `error_handler.py` (tratamento global de exceções HTTP).
     - `src/app.py`: Composition Root da aplicação.
  2. **Extração de Configurações**: Leitura de variáveis de ambiente com fallbacks seguros.
  3. **Segurança e Sanitização**: Parametrização integral de queries SQL, bloqueio de comandos arbitrários em rotas administrativas e hashing de senhas com PBKDF2/Werkzeug.
  4. **Otimização de Performance**: Resolução do gargalo N+1 nas listagens de pedidos via `JOIN`.
  5. **Preservação de Contratos**: Garantia de 100% de compatibilidade com os endpoints, rotas, payloads e status HTTP originais.

---
**Total de Achados**: 11  
**Check de Restrições**: [x] Validado contra `knowledge/constraints.md`  
**Autorização**: Prosseguir com a refatoração automática (Fase 3)? [y/n]  
---
