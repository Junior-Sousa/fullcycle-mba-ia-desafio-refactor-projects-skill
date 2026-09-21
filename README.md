# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento | O que deve conter |
|---|---|
| Análise de projeto | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade |
| Template de relatório | Formato padronizado do relatório de auditoria (Fase 2) |
| Guidelines de arquitetura | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.

---

# 📚 DOCUMENTAÇÃO DO PROCESSO & RELATÓRIO DE ENTREGA

## A) Análise Manual dos Projetos

### 1. `code-smells-project` (Python / Flask + SQLite)
- **[CRITICAL] SQL Injection em Consultas Diretas e Buscas Dinâmicas**: Consultas SQL construídas via f-strings/concatenação (`models.py:28`, `models.py:291`). **Justificativa**: Risco crítico de invasão do banco de dados, bypass de autenticação e manipulação indevida de dados.
- **[CRITICAL] Endpoint Administrativo de Execução de SQL Livre**: Endpoint `POST /admin/query` permitindo comandos DDL/DML arbitrários (`app.py:69`). **Justificativa**: Risco de destruição remota ou roubo completo da base de dados.
- **[CRITICAL] Exposição de Credenciais Hardcoded e Segredos na API**: `SECRET_KEY` exposta em texto puro em `app.py:7`. **Justificativa**: Risco de sequestro de sessão e forjamento de tokens de autenticação.
- **[CRITICAL] God Object / Monolito em `models.py`**: O arquivo `models.py` agregava regras de negócio, persistência SQL, validações e formatação para 4 domínios diferentes. **Justificativa**: Impossibilita isolamento de testes unitários e viola o princípio de responsabilidade única (SRP) do SOLID.
- **[HIGH] Senhas Armazenadas e Comparadas em Texto Puro**: Cadastro e login de usuários sem hashing criptográfico (`database.py:76`). **Justificativa**: Comprometimento direto da privacidade dos usuários em vazamentos de banco.
- **[HIGH] Persistência Vazando na Camada de Transporte**: SQL executado diretamente dentro de handlers de rotas e controllers (`controllers.py:266`). **Justificativa**: Quebra total do padrão MVC e acoplamento entre HTTP e banco de dados.
- **[MEDIUM] Gargalos N+1 em Listagem e Detalhamento de Pedidos**: Iteração no Python buscando itens de cada pedido em queries individuais. **Justificativa**: Exaustão de conexões de I/O e alta latência da API em listas extensas.
- **[MEDIUM] Vazamento de Dados Sensíveis na Serialização**: Método `to_dict()` de usuário expunha a senha nas respostas JSON. **Justificativa**: Violação de privacidade de dados (LGPD).
- **[LOW] Estado Global Mutável e Magic Strings**: Conexões de banco globais e constantes soltas no código. **Justificativa**: Dificuldade de manutenção e risco de vazamento de conexões.

---

### 2. `ecommerce-api-legacy` (Node.js / Express + SQLite)
- **[CRITICAL] Exposição de Credenciais Hardcoded e Log de Cartões**: Chaves de pagamento e banco hardcoded em `utils.js:1` e cartões impressos via `console.log`. **Justificativa**: Violação gravíssima de compliance de segurança de meios de pagamento (PCI-DSS).
- **[CRITICAL] God Object (`AppManager.js`)**: Classe monolítica controlando autenticação, catálogo de cursos, checkout, relatórios e auditoria (`AppManager.js:1-139`). **Justificativa**: Código fortemente acoplado, sem modularidade e impossível de manter.
- **[HIGH] Autenticação Quebrada com Hash Inseguro Customizado**: Uso da função vulnerável `badCrypto` (`utils.js:17`). **Justificativa**: Senhas facilmente reversíveis por força bruta ou ataque de dicionário.
- **[HIGH] Vazamento de Lógica e Persistência na Camada de Transporte**: Consultas SQL de banco dentro da camada de roteamento/controllers. **Justificativa**: Quebra do padrão MVC.
- **[MEDIUM] Callback Hell & Consulta N+1 em Relatório Financeiro**: 4 níveis de callbacks aninhados com consultas SQL iterativas. **Justificativa**: Gargalo severo de performance e propensão a travamentos e memory leaks da API.
- **[MEDIUM] Falta de Integridade Referencial na Deleção de Usuários**: Deleção sem apagar matrículas e pagamentos em cascata. **Justificativa**: Geração de registros órfãos e dados corrompidos no banco de dados.
- **[LOW] Estado Global Mutável em Memória**: Registros de auditoria salvos em array global em memória. **Justificativa**: Perda imediata de logs com o reinício da aplicação.

---

### 3. `task-manager-api` (Python / Flask + Flask-SQLAlchemy)
- **[CRITICAL] Vazamento de Senhas Hasheadas na API**: Dicionário serializado `to_dict()` em `models/user.py` incluía o hash da senha em todas as rotas públicas de usuários. **Justificativa**: Exposição de credenciais dos usuários para qualquer cliente REST.
- **[CRITICAL] Senhas e Credenciais SMTP Hardcoded**: `SECRET_KEY` e credenciais de e-mail expostas em texto puro (`app.py:13`, `services/notification_service.py:10`). **Justificativa**: Exposição de segredos de produção e serviços de mensageria.
- **[CRITICAL] Algoritmo Criptográfico Obsoleto (MD5)**: Senhas salvas utilizando o hash MD5 (`models/user.py:29`). **Justificativa**: Algoritmo MD5 é criptograficamente quebrado e vulnerável a colisão e rainbow tables.
- **[HIGH] Autenticação Quebrada & Token Falso**: Endpoint de login gerando tokens genéricos sem validação rigorosa de credenciais. **Justificativa**: Falha técnica na camada de controle de acesso.
- **[HIGH] Ausência de Controllers & Regras nas Rotas**: Lógica de negócio e queries SQLAlchemy dentro dos arquivos de rotas (`routes/`). **Justificativa**: Acoplamento indevido entre protocolo HTTP e camada de domínio.
- **[MEDIUM] Consultas N+1 em Relatórios e Listagem de Tarefas**: Carregamento lazy de categorias e usuários em cada tarefa listada. **Justificativa**: Ineficiência no acesso a dados e latência desnecessária.
- **[MEDIUM] Ausência de Tratamento Centralizado de Exceções**: Uso de `bare except:` engolindo exceções sem log adequado. **Justificativa**: Ocultação de erros e dificultador de depuração.
- **[LOW] Uso de APIs Depreciadas em Python (`datetime.utcnow()`)**: Chamadas a `datetime.utcnow()` sem fuso horário informado. **Justificativa**: Alertas de depreciação e incompatibilidade futura no Python 3.12+.

---

## B) Construção da Skill (`refactor-arch`)

### 1. Decisões de Design da Skill
A skill foi construída sob uma **arquitetura modular baseada em fases bem delimitadas**:
- **`SKILL.md` (Orquestrador principal)**: Define o fluxo obrigatório em 3 fases:
  - **Fase 1 (Análise)**: Identificação automática da linguagem, framework, ORM/driver de banco e arquitetura existente.
  - **Fase 2 (Auditoria)**: Detecção de achados por severidade, geração do relatório preliminar em `reports/audit-project-{N}.md` e solicitação formal de confirmação ao usuário antes de alterar código.
  - **Fase 3 (Refatoração & Quality Gates)**: Reestruturação do código para MVC+S em `src/`, execução de validações empíricas e atualização final do relatório de auditoria.
- **Conhecimentos Focados em `knowledge/`**:
  - `anti_patterns.md`: Catálogo abrangente com padrões de violações arquiteturais e de segurança (SQL Injection, God Class, MD5, N+1, leaks).
  - `mvc_guidelines.md`: Diretrizes estruturais prescritivas para organização de `src/models`, `src/services`, `src/controllers`, `src/routes`, `src/config` e `src/middlewares`.
  - `refactoring_playbook.md`: Guia de transformações seguras por stack (Python/Flask, Node.js/Express).
  - `report_template.md`: Formatador padronizado de relatórios com placeholders dinâmicos para a auditoria preliminar e final com Quality Gates.
  - `constraints.md` & `analysis.md`: Regras de preservação de contratos de API e lista de verificação de sanidade.

### 2. Catálogo de Anti-patterns Incluídos
- **Segurança**: SQL Injection, Hardcoded Credentials, Weak Cryptography (MD5/badCrypto), Exposição de Senhas em JSON.
- **Arquitetura**: God Object / God Class, Leaking Business Logic in Transport Layer, Absence of Controller Layer.
- **Performance & Qualidade**: N+1 Query Problem, Cascading Deletion Failure, Bare Except / Swallowed Errors, Deprecated Time APIs.

### 3. Abordagem Agnóstica de Tecnologia
A skill foi projetada de forma **independente de stack**:
- **Abstração de Conceitos Arquiteturais**: Em vez de acoplar a skill a sintaxes específicas de uma única linguagem, a skill define o papel semântico de cada camada (`Model` encapsula queries/ORM, `Service` orquestra lógica de negócio, `Controller` trata HTTP `req/res` e `Route` define endpoints).
- **Flexibilidade de Stacks**: Validada com sucesso em ecossistemas Python (Flask com SQLite nativo ou Flask-SQLAlchemy) e Node.js (Express com SQLite nativo).

### 4. Desafios Encontrados e Soluções
- **Desafio**: Manter a estabilidade das APIs sem quebrar contratos durante a migração das rotas para Controllers.
  - *Solução*: Inclusão do arquivo `constraints.md` tornando obrigatória a preservação rigorosa dos endpoints, métodos HTTP e contratos JSON de resposta.
- **Desafio**: Evitar relatórios parciais ou genéricos.
  - *Solução*: Criação de templates de auditoria em duas fases com Quality Gates explícitos (0 erros de lint, Boot Aprovado, 100% Endpoints Aprovados).

---

## C) Resultados da Refatoração

### 1. Resumo dos Achados e Correções (3/3 Projetos Aprovados)

| Projeto | Stack | Severidade dos Achados | Total de Achados | Status de Correção | Health Score Final |
|---|---|---|---|---|---|
| **code-smells-project** | Python / Flask + SQLite | 5 CRITICAL, 2 HIGH, 2 MEDIUM, 2 LOW | 11 Achados | **100% Corrigido (11/11)** | **100 / 100 (Excelente)** |
| **ecommerce-api-legacy** | Node.js / Express + SQLite | 2 CRITICAL, 2 HIGH, 2 MEDIUM, 1 LOW | 7 Achados | **100% Corrigido (7/7)** | **100 / 100 (Excelente)** |
| **task-manager-api** | Python / Flask + SQLAlchemy | 3 CRITICAL, 2 HIGH, 2 MEDIUM, 1 LOW | 8 Achados | **100% Corrigido (8/8)** | **100 / 100 (Excelente)** |

---

### 2. Comparação da Estrutura Antes vs Depois

#### `code-smells-project`
- **Antes**: 4 arquivos monolíticos na raiz (`app.py`, `database.py`, `models.py`, `controllers.py`).
- **Depois**: Arquitetura limpa MVC+S em `src/`:
  - `src/config/settings.py` (Variáveis de ambiente)
  - `src/database/connection.py` (Context manager SQLite)
  - `src/models/` (`produto_model.py`, `usuario_model.py`, `pedido_model.py`, `health_model.py`, `admin_model.py`, `report_model.py`)
  - `src/services/` (`auth_service.py`, `report_service.py`, `health_service.py`, `admin_service.py`)
  - `src/controllers/` (`produto_controller.py`, `usuario_controller.py`, `pedido_controller.py`, `report_controller.py`, `health_controller.py`, `admin_controller.py`)
  - `src/routes/` (`produto_routes.py`, `usuario_routes.py`, `pedido_routes.py`, `report_routes.py`, `health_routes.py`, `admin_routes.py`)

#### `ecommerce-api-legacy`
- **Antes**: 3 arquivos com lógica misturada (`src/app.js`, `src/utils.js`, `src/AppManager.js`).
- **Depois**: Arquitetura limpa MVC+S em `src/`:
  - `src/config/settings.js`
  - `src/database/connection.js`
  - `src/models/` (`UserModel.js`, `CourseModel.js`, `EnrollmentModel.js`, `PaymentModel.js`, `AuditLogModel.js`, `ReportModel.js`)
  - `src/services/` (`CheckoutService.js`, `ReportService.js`)
  - `src/controllers/` (`CheckoutController.js`, `ReportController.js`, `UserController.js`)
  - `src/routes/` (`checkoutRoutes.js`, `reportRoutes.js`, `userRoutes.js`)

#### `task-manager-api`
- **Antes**: Estrutura parcial sem controllers (`models/`, `routes/`, `services/`, `utils/`) com regras de negócio e queries nas rotas.
- **Depois**: Arquitetura padronizada MVC+S em `src/`:
  - `src/config/settings.py`
  - `src/database/connection.py`
  - `src/models/` (`user_model.py`, `task_model.py`, `category_model.py`)
  - `src/services/` (`notification_service.py`, `report_service.py`)
  - `src/controllers/` (`user_controller.py`, `task_controller.py`, `category_controller.py`, `report_controller.py`)
  - `src/routes/` (`user_routes.py`, `task_routes.py`, `report_routes.py`)
  - `src/middlewares/error_handler.py`

---

### 3. Checklist de Aceite Final (Atendido em 3/3 Projetos)

- [x] **Fase 1 detecta a stack corretamente em 3/3 projetos**
- [x] **Fase 2 encontra >= 5 achados em 3/3 projetos** (11 em project-1, 7 em project-2, 8 em project-3)
- [x] **Fase 2 inclui pelo menos 1 CRITICAL ou HIGH em 3/3 projetos**
- [x] **Fase 3 aplicação funciona perfeitamente após a refatoração em 3/3 projetos** (Boot Check OK, 0 erros de lint/sintaxe, 100% endpoints responsivos)

---

## D) Como Executar

### 1. Pré-requisitos
- Python 3.10+ (para `code-smells-project` e `task-manager-api`)
- Node.js 18+ (para `ecommerce-api-legacy`)
- Antigravity / AGY CLI / Claude Code instalado e configurado na máquina

### 2. Comandos para Executar a Skill em Cada Projeto

#### Projeto 1 (`code-smells-project`)
```bash
cd code-smells-project
# Executar a skill refactor-arch
/refactor-arch
```

#### Projeto 2 (`ecommerce-api-legacy`)
```bash
cd ../ecommerce-api-legacy
# Executar a skill refactor-arch
/refactor-arch
```

#### Projeto 3 (`task-manager-api`)
```bash
cd ../task-manager-api
# Executar a skill refactor-arch
/refactor-arch
```

---

### 3. Como Validar que a Refatoração Funcionou

#### Validação do Projeto 1 (`code-smells-project`)
```bash
cd code-smells-project
python3 app.py
# Testar endpoint de health
curl http://localhost:5000/health
```

#### Validação do Projeto 2 (`ecommerce-api-legacy`)
```bash
cd ecommerce-api-legacy
npm start
# Ou rodar o servidor em background
node src/app.js
```

#### Validação do Projeto 3 (`task-manager-api`)
```bash
cd task-manager-api
python3 app.py
# Popular banco e testar API
python3 seed.py
curl http://localhost:5000/health
```