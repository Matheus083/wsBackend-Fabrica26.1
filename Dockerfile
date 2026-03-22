# 1. Usa uma imagem leve do Python
FROM python:3.12-slim

# 2. Define variáveis de ambiente para o Python não criar arquivos .pyc e não segurar logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Define a pasta de trabalho dentro do container
WORKDIR /app

# 4. Instala dependências do sistema (necessárias para o PostgreSQL e outras libs)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise

# 6. Copia o resto do código para dentro do container
COPY . .

# 7. Coleta arquivos estáticos (CSS, JS)
RUN python manage.py collectstatic --noinput

# 8. Comando para iniciar o servidor usando Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]