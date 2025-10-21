# 🧱 **Athos Monitor — Testes Não Funcionais com Docker Swarm**

## 📂 **Estrutura do Projeto**

| Pasta / Arquivo                | Função                                                |
| ------------------------------ | ----------------------------------------------------- |
| `app/`                         | Código Flask (API com usuários e produtos)            |
| `tests/`                       | Arquivos Locust + testes Pytest                       |
| `Dockerfile`, `wait-for-db.sh` | Build e inicialização da aplicação                    |
| `docker-compose.yml`           | Execução simples (sem Swarm)                          |
| `docker-stack.yml`             | Execução via **Swarm** (com limites de CPU e memória) |
| `README_SWARM.txt`             | Instruções completas                                  |
| `requirements.txt`             | Dependências Python                                   |


## 🧭 **PASSO A PASSO — Docker Swarm com Limites de Recursos**

### 🔹 **1️⃣ Inicializar o Docker Swarm (apenas 1x na máquina)**

Abra o PowerShell **como administrador** e execute:

```bash
docker swarm leave --force
docker swarm init
```


### 🔹 **2️⃣ Construir a imagem local do app**

Antes de subir o stack, construa a imagem local que o Swarm usará:

```bash
docker build -t athos_app_image:latest .
```


### 🔹 **3️⃣ Fazer o deploy do stack**

Cria 3 serviços com limites de CPU e memória definidos:

```bash
docker stack deploy -c docker-stack.yml athos
```


### 🔹 **4️⃣ Verificar os serviços em execução**

```bash
docker stack services athos
```

Você deve ver algo como:

```
ID                  NAME                 MODE        REPLICAS   IMAGE
xxxxxxx             athos_db             replicated  1/1        postgres:16
xxxxxxx             athos_web            replicated  1/1        athos_app_image:latest
xxxxxxx             athos_locust         replicated  1/1        locustio/locust:2.32.0
```


### 🔹 **5️⃣ Acessar as aplicações**

* **API:** [http://localhost:5000/usuarios](http://localhost:5000/usuarios)
* **Locust (stress test):** [http://localhost:8089](http://localhost:8089)


## 🧪 **TESTES SOLICITADOS PELO PROFESSOR**

### 🧩 **1️⃣ Teste de Performance**

Avalia o tempo de resposta e estabilidade sob carga leve.

**No Locust:**

* **Host:** `http://web:5000`
* **Users:** `50`
* **Spawn rate:** `5`

✅ *Objetivo:* medir tempo médio de resposta (ideal: abaixo de 500 ms).


### 🧩 **2️⃣ Teste de Stress**

Força o limite da CPU/memória até provocar falha.

**No Locust:**

* **Users:** `800`
* **Spawn rate:** `15`

Em outro terminal, acompanhe o consumo:

```bash
docker stats
```

➡️ O container `athos_web` tem limite de:

* **CPU:** 0.5 core
* **Memória:** 512 MB

🧠 **Comportamento esperado:**

* O uso atinge 100% de CPU/memória;
* O app começa a lançar erros 500;
* O Docker pode reiniciar o serviço automaticamente (crash controlado).


### 🧩 **3️⃣ Teste de Fail & Recovery**

#### 🧨 **(a) Queda do Banco**

Durante o stress test, simule uma falha no banco:

```bash
docker service scale athos_db=0
```

➡️ O app começa a lançar erros `500 / database unavailable`.

Traga o banco de volta:

```bash
docker service scale athos_db=1
```

➡️ O sistema se recupera automaticamente — Locust volta a exibir respostas `200 OK`.


#### 🔁 **(b) Reinício do App (Fail & Recovery Interno)**

Durante o stress test, simule o reinício inesperado do serviço principal:

```bash
docker service update --force athos_web
```

➡️ O container `athos_web` será reiniciado — parte das requisições falhará por alguns segundos.
➡️ Assim que o serviço voltar, o Locust retomará as respostas `200 OK`.

✅ Esse é o teste clássico de **Fail & Recovery interno**, mostrando a resiliência do ambiente sob orquestração.


### 🧩 **4️⃣ Teste de Resiliência e Monitoramento**

**Ver logs recentes:**

```bash
docker service logs athos_web --since 1m
```

**Monitorar uso de recursos:**

```bash
docker stats
```


### 🧹 **Encerrar o ambiente (limpeza final)**

```bash
docker stack rm athos
docker volume rm athos_db_data
```


## 🧠 **Resumo do Comportamento Esperado**

| Tipo de Teste       | Objetivo                                 | Resultado Esperado                                     |
| ------------------- | ---------------------------------------- | ------------------------------------------------------ |
| **Performance**     | Verificar estabilidade                   | API responde <500 ms                                   |
| **Stress**          | Forçar o sistema a falhar por sobrecarga | App atinge limite de CPU/memória, travando/reiniciando |
| **Fail & Recovery** | Simular queda real                       | App e banco caem e se recuperam automaticamente        |
| **Resiliência**     | Medir estabilidade após falha            | Sistema retoma respostas 200 OK                        |

