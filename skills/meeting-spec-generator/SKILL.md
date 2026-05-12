---
name: meeting-spec-generator (1)
version: 1.0.1-validated
author: <preencher>
reviewed_by: Cateno Skill Validator
approved_by: <Seguranca da Informacao Cateno -- obrigatorio>
security_level: validated
last_reviewed: 2026-05-12
compliance: LGPD-aware
---

# SECURITY NOTES

- Nao passe CPF, nome, conta, dados de cartao ou qualquer dado pessoal como input
- Nao passe credenciais, tokens, senhas ou chaves de API como argumentos
- Use apenas em projetos autorizados pela area de Seguranca Cateno
- Inputs sao validados antes de qualquer processamento
- Conformidade LGPD: esta skill nao deve ser usada para armazenar dados pessoais

# DATA PRIVACY

Esta skill nao processa dados pessoais de portadores de cartao.
Para uso com dados pessoais, obtenha aprovacao previa do DPO Cateno.

# meeting-spec-generator (1)

[Conteudo original com correcoes de seguranca aplicadas]

## Validacao de Inputs

Todos os argumentos passados para esta skill sao validados:
- Tipo verificado antes do uso
- Comprimento maximo imposto
- Formato validado via regex
- Caminhos de arquivo verificados para nao ultrapassar o diretorio do projeto

## Escopo de Acesso

Esta skill opera exclusivamente dentro do diretorio do projeto.
Qualquer tentativa de acesso a caminhos externos e rejeitada automaticamente.
