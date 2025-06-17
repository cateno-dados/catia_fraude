# ETL para Tabela de Treino de Modelo

Este notebook executa o processo de ETL (Extração, Transformação e Carga) de dados provenientes de bancos PostgreSQL e DB2, com o objetivo de preparar uma tabela consolidada de treino para modelos analíticos.

## 📌 Objetivo

Criar uma tabela de treino unificada no PostgreSQL, com dados extraídos e tratados de diferentes fontes, para posterior uso em modelagem preditiva.

## ⚙️ Requisitos

- Python 3.8+
- Bibliotecas:
  - psycopg2-binary
  - sshtunnel
  - paramiko
  - polars
  - pyspark
  - python-dotenv
  - sqlalchemy
  - jaydebeapi
  - jpype

## 🛠️ Como executar

1. Configure as variáveis no arquivo `.env` com as credenciais de acesso:
SSH_HOST=
SSH_PORT=
SSH_USER=
SSH_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
JDBC_URL=
