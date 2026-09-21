# Conhecimento: Template de Relatório de Auditoria Profissional

Este template deve ser rigorosamente seguido na geração dos relatórios de auditoria de arquitetura (Fase 2). **Regra Obrigatória**: Cada achado computado na tabela de métricas deve ter uma entrada detalhada correspondente na Seção 2, totalizando **no mínimo 5 findings detalhados** por projeto.

---

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
- **Impacto de Negócio**: {Consequências para o negócio: risco de vazamento, corrupção de dados, custos de nuvem ou lentidão}
- **Recomendação Arquitetural**: {Diretriz prescritiva de refatoração seguindo o padrão MVC e o Playbook}

### [{SEVERIDADE}] {Título do Achado 2}
- **Localização**: `{arquivo}:{linhas}`
- **Padrão**: {Nome do anti-padrão conforme knowledge/anti_patterns.md}
- **Análise**: {Explicação técnica}
- **Impacto de Negócio**: {Impacto}
- **Recomendação Arquitetural**: {Recomendação}

### [{SEVERIDADE}] {Título do Achado 3}
- **Localização**: `{arquivo}:{linhas}`
- **Padrão**: {Nome do anti-padrão conforme knowledge/anti_patterns.md}
- **Análise**: {Explicação técnica}
- **Impacto de Negócio**: {Impacto}
- **Recomendação Arquitetural**: {Recomendação}

### [{SEVERIDADE}] {Título do Achado 4}
- **Localização**: `{arquivo}:{linhas}`
- **Padrão**: {Nome do anti-padrão conforme knowledge/anti_patterns.md}
- **Análise**: {Explicação técnica}
- **Impacto de Negócio**: {Impacto}
- **Recomendação Arquitetural**: {Recomendação}

### [{SEVERIDADE}] {Título do Achado 5}
- **Localização**: `{arquivo}:{linhas}`
- **Padrão**: {Nome do anti-padrão conforme knowledge/anti_patterns.md}
- **Análise**: {Explicação técnica}
- **Impacto de Negócio**: {Impacto}
- **Recomendação Arquitetural**: {Recomendação}

---

## 3. Arquitetura Alvo Proposta
- **Padrão**: Model-View-Controller (MVC) + Camada de Serviço (se aplicável)
- **Plano de Refatoração**:
  1. Criação da estrutura de pastas padronizada (`src/models`, `src/controllers`, `src/routes`, `src/config`).
  2. Extração de configurações e variáveis de ambiente.
  3. Desacoplamento da persistência e correção de vulnerabilidades de segurança (parametrização de SQL, proteção/bloqueio de SQL livre em admin, modernização de hashing).
  4. Extração de regras de negócio para Services e Controllers enxutos.
  5. Centralização do roteamento e tratamento de erros.
- **Padronização**: {Descrever padrão de nomenclatura e organização adotados}

---
**Total de Achados**: {total >= 5}  
**Check de Restrições**: [x] Validado contra `knowledge/constraints.md`  
**Autorização**: Prosseguir com a refatoração automática (Fase 3)? [y/n]  
---
