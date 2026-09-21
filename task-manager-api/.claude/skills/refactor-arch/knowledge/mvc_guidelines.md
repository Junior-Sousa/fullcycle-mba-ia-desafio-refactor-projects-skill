# Conhecimento: Diretrizes Universais MVC+S

Diretrizes de arquitetura para refatoração profissional, adaptáveis a diferentes ecossistemas.

## 1. Camadas e Responsabilidades

### 📦 Configuração (Transversal)
- **Função**: Centralizar variáveis de ambiente, configurações de infraestrutura e injeção de dependências inicial.
- **Exemplos**: `src/config/`, `internal/config/`, `application.yml`.

### 🏗️ Models (Domínio/Dados)
- **Função**: Representar as entidades de negócio e a persistência.
- **Regra**: Deve ser agnóstico à interface (CLI, Web, Mobile). Não deve conter lógica de IO de rede.

### ⚙️ Services (Lógica de Negócio) - *Opcional mas Recomendado*
- **Função**: Orquestrar lógica complexa que envolve múltiplos Models ou serviços externos.
- **Regra**: Onde mora a "verdade" do negócio.

### 🎮 Controllers (Orquestração)
- **Função**: Ponte entre a requisição externa e a lógica interna.
- **Regra**: Camada "fina". Recebe entrada, chama Service/Model, devolve resposta.

### 🛣️ Rotas / Adaptadores (Interface)
- **Função**: Mapear os entrypoints da aplicação para as ações dos controladores.

## 2. Padrões de Diretórios por Ecossistema

- **Python/Flask/Django**: `src/models/`, `src/controllers/`, `src/routes/`.
- **Node.js/TS**: `src/models/`, `src/controllers/`, `src/routes/` ou `src/modules/`.
- **Go (Standard Layout)**: `internal/handler/` (controllers), `internal/repository/` (models), `internal/service/`.
- **Java (Standard Package)**: `com.company.project.domain`, `com.company.project.controller`, `com.company.project.service`.

## 3. Princípios de Sucesso
1. **Separação de Preocupações (SoC)**: Cada arquivo faz apenas uma coisa.
2. **Dependência para Abstração**: Utilizar interfaces ou classes base quando possível.
3. **Imutabilidade**: Preferir objetos imutáveis para transporte de dados (DTOs).
