# Guia de Instalação do Projeto

## Sobre este documento

Este documento descreve **o passo a passo de instalação do projeto**, reunindo todos os processos necessários de forma **autocontida**.

---

## Passo a passo de instalação

### 1. Download do dataset

Acesse o link abaixo e faça o download do dataset:

- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

> **Observação:** é necessário ter uma conta no Kaggle para realizar o download.

---

### 2. Extração dos arquivos

Após o download:

1. Extraia o conteúdo do arquivo baixado para dentro da pasta [database/olist_data](../../database/init/olist_data/).
2. Verifique se a extração gerou **exatamente 9 arquivos `.csv`**.

Se a quantidade de arquivos for diferente, revise o processo de extração antes de prosseguir.

---

### 3. Configuração do Docker Compose

Na **raiz do projeto**, renomeie o arquivo:


* `docker-compose.example.yml`  → `docker-compose.yml`


--- 

### 4. Configuração dos arquivos de ambiente e Dockerfiles

Realize as seguintes renomeações na pasta `back/`:

1. `dockerfile.example` → `dockerfile`

2. `.env.example` → `.env`

E na pasta `database/`:

1. `dockerfile.example` → `dockerfile`


--- 

### 5. Subida dos containers

Com tudo configurado, execute o comando abaixo na raiz do projeto:

```bash
docker compose up
```

Esse comando irá construir as imagens e iniciar todos os serviços necessários para o funcionamento do projeto.

## Parabéns! 

Você concluiu a instalação do projeto. A continuação da documentação do projeto está distribuída em diferentes pastas neste repositório. Para um guia do que explorar agora, veja [aqui](../../README.md)