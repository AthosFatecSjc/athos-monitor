from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def listar_usuarios(self):
        self.client.get("/usuarios")

    @task(1)
    def criar_usuario(self):
        self.client.post("/usuarios", json={"nome": "Usuário Stress Test"})
