# Installation Guide

## About this document

This document describes the **step-by-step installation of the project**, bringing together all the necessary processes in a **self-contained** way.

---

## Installation Step-by-Step

### 1. Download the data

Access the link below and download the dataset:

- https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

> **Note:** A Kaggle account is required to download the data.

---

### 2. File Extraction

After downloading:

1. Extract the contents of the downloaded file inside the folder [database/olist_data](../../database/init/olist_data/).
2. Verify that the extraction generated **exactly 9 `.csv` files**.

If the number of files is different, review the extraction process before proceeding.

---

### 3. Docker Compose Configuration

In the **project root**, rename the file:

* `docker-compose.example.yml`  → `docker-compose.yml`

--- 

### 4. Environment Files and Dockerfiles Configuration

Perform the following renames in the `back/` folder:

1. `dockerfile.example` → `dockerfile`

2. `.env.example` → `.env`

And in the `database/` folder:

1. `dockerfile.example` → `dockerfile`

--- 

### 5. Starting the Containers

With everything configured, run the command below in the project root:

```bash
docker compose up
```

This command will build the images and start all the services required for the project to run.


## Congratulations! 

You have completed the project installation. The rest of the project documentation is distributed across different folders in this repository. For a guide on what to explore now, see [here](../../README.md)