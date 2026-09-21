# Conhecimento: Template de Relatório de Auditoria Profissional

Este documento define os formatos para os relatórios de auditoria de arquitetura em cada fase. **Regra Obrigatória**: Cada achado computado na tabela de métricas deve ter uma entrada detalhada correspondente na Seção 2, totalizando **no mínimo 5 findings detalhados** por projeto.

---

## 1. Template da Fase 2 (Auditoria Inicial e Pedido de Aprovação)

Use este formato ao gerar o relatório em `reports/audit-project-{N}.md` ao final da Fase 2:

```markdown
# AUDITORIA ARQUITETURAL & AVALIAÇÃO TÉCNICA
**Projeto**: {Nome do Projeto}  
**Arquiteto**: Especialista Refactor-Arch  
**Data da Avaliação**: {Data Atual: YYYY-MM-DD}  
**Visão Geral da Stack**: {Linguagem} | {Framework} | {Banco de Dados}  

## 1. Resumo Executivo
{Parágrafo contextualizando a situação arquitetural da base legada, o nível de débito técnico encontrado e os principais riscos operacionais, de segurança e de manutenibilidade.}

**Tabela de Métricas**:
| Severidade | Contagem | Nível de Impacto |
|---|---|---|
| **CRITICAL** | {n} | Alto Risco / Ação Imediata |
| **HIGH** | {n} | Débito Estrutural / Risco de Segurança |
| **MEDIUM** | {n} | Performance / Manutenibilidade |
| **LOW** | {n} | Code Smell / Boas Práticas |

---

## 2. Achados Detalhados
*(Todos os findings contados na tabela acima devem ser obrigatoriamente detalhados nesta seção, mínimo 5)*

### [{SEVERIDADE}] {Título do Achado 1}
- **Localização**: `{arquivo}:{linhas}`
- **Padrão**: {Nome do anti-padrão conforme knowledge/anti_patterns.md}
- **Análise**: {Explicação técnica e factual da violação encontrada no código}
- **Impacto de Negócio**: {Consequências para o negócio}
- **Recomendação Arquitetural**: {Diretriz prescritiva de refatoração}

---

## 3. Arquitetura Alvo Proposta
- **Padrão**: Model-View-Controller (MVC) + Camada de Serviço (se aplicável)
- **Plano de Refatoração**:
  1. Criação da estrutura de pastas padronizada (`src/models`, `src/controllers`, `src/routes`, `src/config`).
  2. Extração de configurações e variáveis de ambiente.
  3. Desacoplamento da persistência e correção de vulnerabilidades de segurança.
  4. Extração de regras de negócio para Services e Controllers enxutos.
  5. Centralização do roteamento e tratamento de erros.

---
**Total de Achados**: {total >= 5}  
**Check de Restrições**: [x] Validado contra `knowledge/constraints.md`  
**Autorização**: Prosseguir com a refatoração automática (Fase 3)? [y/n]  
```

---

## 2. Template da Fase 3 (Relatório Pós-Refatoração Final)

Após concluir a Fase 3 e validar os Quality Gates, atualize o arquivo em `reports/audit-project-{N}.md` para o formato final:

```markdown
# AUDITORIA ARQUITETURAL & AVALIAÇÃO TÉCNICA
**Projeto**: {Nome do Projeto}  
**Arquiteto**: Especialista Refactor-Arch  
**Data da Avaliação**: {Data Atual: YYYY-MM-DD}  
**Visão Geral da Stack**: {Linguagem} | {Framework} | {Banco de Dados}  

## 1. Resumo Executivo
{Parágrafo resumindo a arquitetura original e a nova estrutura MVC+S implementada em src/, com a confirmação da correção de todos os achados.}

**Tabela de Métricas (Status de Correção)**:
| Severidade | Contagem | Status de Correção | Nível de Impacto Final |
|---|---|---|---|
| **CRITICAL** | {n} | 100% Corrigido ({n}/{n}) | Mitigado / Seguro |
| **HIGH** | {n} | 100% Corrigido ({n}/{n}) | Resolvido / Arquitetura Limpa |
| **MEDIUM** | {n} | 100% Corrigido ({n}/{n}) | Otimizado / Alta Performance |
| **LOW** | {n} | 100% Corrigido ({n}/{n}) | Padronizado / Boas Práticas |

---

## 2. Achados Detalhados e Status de Correção

### [{SEVERIDADE}] {Título do Achado 1}
- **Localização Original**: `{arquivo}:{linhas}`
- **Localização Refatorada**: `{novo_arquivo}:{linhas}`
- **Status**: **CORRIGIDO & VALIDADO**
- **Análise & Solução**: {Explicação da violação original e como a solução refatorada a resolveu}

---

## 3. Arquitetura Final Implementada
- **Padrão**: Model-View-Controller com Camada de Serviço (MVC+S)
- **Estrutura de Pastas**:
  - `src/config/`: Configurações centralizadas
  - `src/database/`: Conexão com banco
  - `src/models/`: Entidades de dados
  - `src/services/`: Lógicas de negócio e relatórios
  - `src/controllers/`: Controladores enxutos
  - `src/routes/`: Blueprints de rotas
  - `src/middlewares/`: Tratamento centralizado de erros
  - `app.py`: Composition Root

---

## 4. Resultado da Avaliação (Quality Gates)
- **Erros de Sintaxe / Lint**: {0 Erros ou contagem de erros}
- **Execução da Aplicação (Boot Check)**: {APROVADO / REPROVADO}
- **Validação de Endpoints da API**: {100% Aprovado / porcentagem de sucesso}
- **Health Score Final**: **{Score Final: ex: 100 / 100 (Excelente)}**

---
**Total de Achados Processados**: {total >= 5}  
**Status Final**: Refatoração concluída e validada com sucesso.  
```
