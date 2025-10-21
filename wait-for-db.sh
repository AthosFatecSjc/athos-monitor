#!/bin/sh
echo "⏳ Aguardando o banco de dados iniciar..."
for i in $(seq 1 30); do
  nc -z db 5432 && echo "✅ Banco de dados disponível!" && break
  echo "Tentativa $i: aguardando..."
  sleep 2
done
echo "🚀 Iniciando aplicação Flask..."
flask run --host=0.0.0.0 --port=5000
