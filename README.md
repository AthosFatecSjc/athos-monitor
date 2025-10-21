
| Pasta / Arquivo                | Função                                                |
| ------------------------------ | ----------------------------------------------------- |
| `app/`                         | Código Flask (API com usuários e produtos)            |
| `tests/`                       | Arquivos Locust + testes Pytest                       |
| `Dockerfile`, `wait-for-db.sh` | Build e inicialização da aplicação                    |
| `docker-compose.yml`           | Execução simples (sem Swarm)                          |
| `docker-stack.yml`             | Execução via **Swarm** (com limites de CPU e memória) |
| `README_SWARM.txt`             | Instruções completas                                  |
| `requirements.txt`             | Dependências Python                                   |

---

## 🧭 **PASSO A PASSO — Docker Swarm com Limites de Recursos**

### 🔹 **1️⃣ Inicializar o Docker Swarm (apenas 1x na máquina)**

Abra o PowerShell como administrador e rode:

```bash
docker swarm init
```

---

### 🔹 **2️⃣ Construir a imagem local do app**

Antes de subir o stack, precisamos criar a imagem que o Swarm usará:

```bash
docker build -t athos_app_image:latest .
```

---

### 🔹 **3️⃣ Fazer o deploy do stack**

Isso cria 3 serviços com limites de CPU/memória definidos:

```bash
docker stack deploy -c docker-stack.yml athos
```

---

### 🔹 **4️⃣ Verificar os serviços em execução**

```bash
docker stack services athos
```

Você verá algo como:

```
ID                  NAME                 MODE        REPLICAS   IMAGE
xxxxxxx             athos_db             replicated  1/1        postgres:16
xxxxxxx             athos_web            replicated  1/1        athos_app_image:latest
xxxxxxx             athos_locust         replicated  1/1        locustio/locust:2.32.0
```

---

### 🔹 **5️⃣ Acessar as aplicações**

* API → [http://localhost:5000/usuarios](http://localhost:5000/usuarios)
* Locust (stress test) → [http://localhost:8089](http://localhost:8089)

---

## 🧪 **TESTES SOLICITADOS PELO PROFESSOR**

### 🧩 **1️⃣ Teste de Performance**

Verifica tempo de resposta e estabilidade sob carga leve.

No Locust:

* **Host:** `http://web:5000`
* **Users:** `50`
* **Spawn rate:** `5`

➡️ Observe o tempo médio de resposta (ideal: < 500ms).

---

### 🧩 **2️⃣ Teste de Stress**

Força o limite da CPU/memória até falha.

1️⃣ Ajuste no Locust:

* **Users:** `300`
* **Spawn rate:** `30`

2️⃣ Em outro terminal, monitore:

```bash
docker stats
```

➡️ O container `athos_web` (Flask) tem limite de:

* **CPU:** 0.5 core
* **Memória:** 512MB

Quando o uso atinge 100%, o Docker pode:

* Retornar erros 500 (app travando);
* Reiniciar o serviço automaticamente (comportamento de crash controlado).

---

### 🧩 **3️⃣ Teste de Fail & Recovery**

Durante o stress, simule uma queda real do banco.

1️⃣ Derrube o banco:

```bash
docker service scale athos_db=0
```

➡️ O app começa a lançar erros (500 / “database unavailable”).

2️⃣ Traga o banco de volta:

```bash
docker service scale athos_db=1
```

➡️ O sistema se recupera automaticamente — Locust volta a exibir sucesso (200 OK).

---

### 🧩 **4️⃣ Teste de Resiliência e Monitoramento**

* Ver logs:

```bash
docker service logs athos_web --since 1m
```

* Ver consumo:

```bash
docker stats
```

---

### 🧹 **Encerrar o ambiente (limpar tudo)**

```bash
docker stack rm athos
docker volume rm athos_db_data
```

---

## 🧠 **Resumo do Comportamento Esperado**

| Tipo de Teste       | Objetivo                                 | Resultado Esperado                                     |
| ------------------- | ---------------------------------------- | ------------------------------------------------------ |
| **Performance**     | Verificar estabilidade                   | API responde <500ms                                    |
| **Stress**          | Forçar o sistema a falhar por sobrecarga | App atinge limite de CPU/memória, travando/reiniciando |
| **Fail & Recovery** | Simular queda real                       | App falha e se recupera após retorno do banco          |
| **Resiliência**     | Medir estabilidade após falha            | Sistema retoma respostas 200 OK                        |

