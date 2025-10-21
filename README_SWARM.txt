ATHOS MONITOR - Docker Swarm & Resource Limits (Windows)

Objetivo:
Este documento mostra como usar Docker Swarm (ou deploy com resource limits) para isolar recursos e garantir que você consiga
forçar a falha do serviço athos-app durante um stress test controlado.

Observações importantes:
- No Docker Desktop Windows, você precisa habilitar Swarm (docker swarm init) e garantir que o Docker Desktop CPU/memory settings sejam suficientes.
- Resource limits funcionam melhor no modo Swarm (docker stack deploy) porque o campo 'deploy.resources' é ignorado pelo 'docker compose up' sem swarm.

Passo a passo (modo simples usando docker compose com limites):
1) Se preferir não usar Swarm, edite o docker-compose.yml e adicione limites usando 'deploy' (note: deploy é respeitado em Swarm).
   Exemplos (usando docker-stack.yml com deploy.resources):
   - athos-app: cpus 0.5, memory 512M
   - locust: cpus 1.0, memory 1024M

Modo A - Usando Docker Swarm (recomendado):
------------------------------------------
1. Abra PowerShell como administrador.
2. Inicie o swarm (apenas uma vez por máquina):
   > docker swarm init
3. Construa a imagem do app localmente (para o stack usar):
   > docker build -t athos_app_image:latest .
4. Deploy do stack usando o arquivo docker-stack.yml:
   > docker stack deploy -c docker-stack.yml athos
5. Verifique serviços:
   > docker stack services athos
6. Acesse a API e o Locust:
   - API: http://localhost:5000/usuarios
   - Locust: http://localhost:8089

Limitação de CPU e memória:
- O stack define athos-app com cpus: 0.5 (meia CPU) e memory 512M (limite).
- Assim, sob carga, athos-app deverá esgotar CPU/ memória e falhar/reiniciar — controlando o ambiente de teste.

Para remover o stack e limpar:
> docker stack rm athos
> docker volume rm athos_db_data (se quiser apagar dados)

Modo B - Usando docker-compose (sem Swarm):
------------------------------------------
Se não for usar Swarm, você pode limitar recursos no Docker Desktop settings (per-container limits não são aplicados via docker-compose v3).
Outra alternativa é usar 'docker run' com flags --cpus e --memory para rodar containers manualmente.

Dicas adicionais:
- Use 'docker stats' para monitorar consumo.
- Ajuste os limites (cpus/memory) para calibrar o ponto de falha que deseja demonstrar.
- Se o Locust estiver consumindo muita CPU, reduza a CPU alocada para ele ou execute Locust em outra máquina/VM.

Boa apresentação!