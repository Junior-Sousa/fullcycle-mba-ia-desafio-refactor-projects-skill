# Conhecimento: Restrições & Limites (Guardrails)

Diretrizes de segurança e limites operacionais para a skill de refatoração.

## 1. Preservação de Contrato (Estabilidade de API)
- **NÃO ALTERAR**: Assinaturas de endpoints públicos (URLs, métodos HTTP, estruturas de JSON de entrada/saída) a menos que explicitamente solicitado. A refatoração é estrutural interna, não funcional externa.
- **NÃO REMOVER**: Documentação técnica existente (docstrings, JSDoc, comentários de lógica complexa).

## 2. Limites de Modificação
- **ARQUIVAMENTO**: Sempre renomear arquivos legados (ex: `.legacy` ou `.old`) em vez de deletá-los imediatamente.
- **DEPENDÊNCIAS**: Não instalar novas bibliotecas globais sem verificar o gerenciador de pacotes local. Preferir bibliotecas já presentes no projeto.
- **MIGRAÇÃO DE DADOS**: Não alterar o esquema do banco de dados (tabelas/colunas) de forma destrutiva. Migrações devem ser apenas aditivas ou de normalização básica.

## 3. Segurança (Redlines)
- **SENHAS**: Nunca imprimir hashes de senhas em logs ou no relatório de auditoria.
- **SEGREDOS E FALLBACKS**: Nunca mover segredos para variáveis de ambiente mantendo a chave secreta legada/vazada como valor padrão (`default`) de `os.getenv` / `process.env`. O valor de fallback para ambiente de desenvolvimento deve ser estritamente genérico (ex: `"dev-insecure-secret-key-change-in-production"`).
- **TOKENS DE AUTENTICAÇÃO**: Nunca retornar tokens fictícios, estáticos ou não assinados na autenticação (ex: `"jwt-token-1"`, `"fake-token"`). O token de resposta deve ser assinado criptograficamente via HMAC-SHA256 (HS256) utilizando a `SECRET_KEY` da aplicação e contendo claims estruturadas (`user_id`, `iat`, `exp`).
