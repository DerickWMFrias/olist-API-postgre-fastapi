# Guia de Instalação do Projeto

## Sobre este documento

Este documento descreve **o passo a passo de instalação do projeto**, reunindo todos os processos necessários de forma **autocontida**. Ele deve ser mantido nesta pasta específica da documentação para facilitar a reprodução do ambiente por qualquer pessoa que clone o repositório.

---

## Passo a passo de instalação

### 1. Download do dataset

Acesse o link abaixo e faça o download do dataset:

- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

> **Observação:** é necessário ter uma conta no Kaggle para realizar o download.

---

### 2. Extração dos arquivos

Após o download:

1. Extraia o conteúdo do arquivo baixado **para esta mesma pasta onde este markdown está localizado**.
2. Verifique se a extração gerou **exatamente 9 arquivos `.csv`**.

Se a quantidade de arquivos for diferente, revise o processo de extração antes de prosseguir.

---

### 3. Configuração do Docker Compose

Na **raiz do projeto**, renomeie o arquivo:

```bash
docker-compose.example.yml
```

--- 

### 4. Configuração dos arquivos de ambiente e Dockerfiles

Realize as seguintes renomeações na pasta back/:

1. dockerfile.example → dockerfile

2. .env.example → .env

Na pasta database/:

1. dockerfile.example → dockerfile

--- 

### 5. Subida dos containers

Com tudo configurado, execute o comando abaixo na raiz do projeto:

```bash
docker compose up
```

Esse comando irá construir as imagens e iniciar todos os serviços necessários para o funcionamento do projeto.