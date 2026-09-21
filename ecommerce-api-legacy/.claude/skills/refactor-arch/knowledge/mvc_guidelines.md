# Conhecimento: Diretrizes Universais MVC+S

Diretrizes de arquitetura para refatoração profissional, adaptáveis a diferentes ecossistemas.

## 1. Camadas e Responsabilidades

### 📦 Configuração (Transversal)
- **Função**: Centralizar variáveis de ambiente, configurações de infraestrutura e injeção de dependências inicial.
- **Exemplos**: `src/config/`, `internal/config/`, `application.yml`.

### 🏗️ Models (Domínio/Dados)
- **Função**: Representar as entidades de negócio e encapsular a persistência de dados.
- **Regra**: **Toda e qualquer instrução SQL ou acesso direto a banco de dados DEVE residir na camada de Model**. Deve ser agnóstico à interface (CLI, Web, Mobile) e não conter lógica de IO de rede.

### ⚙️ Services (Lógica de Negócio e Orquestração) - *Orientado à Complexidade (Sem Overengineering)*
- **Função**: Orquestrar lógicas complexas que envolvem múltiplos Models, regras de negócio pesadas (ex: cálculo de descontos, relatórios) ou integração com infraestrutura/configuração.
- **Regra**: Aplicar onde mora a "verdade" de negócio ou agregação multifuncional. Para CRUDs simples de uma única entidade, o Controller pode chamar diretamente o Model sem a necessidade de Services intermediários "passa-bastão" (`Controller ➔ Model`), evitando overengineering.

### 🎮 Controllers (Orquestração de Transporte)
- **Função**: Ponte entre a requisição externa (HTTP/CLI) e a lógica interna da aplicação.
- **Regra**: Camada "fina". Trata recepção/validação HTTP, invoca o Model (para CRUDs simples) ou o Service (para orquestração/regras complexas) e devolve a resposta formatada (JSON, status code). **Zero código SQL ou chamadas diretas de conexões de banco de dados nos Controllers**.

### 🛣️ Rotas / Adaptadores (Interface)
- **Função**: Mapear os entrypoints da aplicação para as ações dos controladores.

## 2. Padrões de Diretórios por Ecossistema

- **Python/Flask/Django**: `src/models/`, `src/controllers/`, `src/routes/`, `src/services/`.
- **Node.js/TS**: `src/models/`, `src/controllers/`, `src/routes/`, `src/services/` ou `src/modules/`.
- **Go (Standard Layout)**: `internal/handler/` (controllers), `internal/repository/` (models), `internal/service/`.
- **Java (Standard Package)**: `com.company.project.domain`, `com.company.project.controller`, `com.company.project.service`.

## 3. Princípios de Sucesso
1. **Separação de Preocupações (SoC)**: Cada arquivo faz apenas uma coisa.
2. **Pragmatismo Sem Overengineering**: Usar Services apenas quando houver orquestração ou regra de negócio complexa.
3. **Dependência para Abstração**: Utilizar interfaces ou classes base quando possível.
4. **Imutabilidade**: Preferir objetos imutáveis para transporte de dados (DTOs).
