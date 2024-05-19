# Utilisez une image de base Python officielle
FROM python:3.12-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers requis pour l'installation des dépendances
COPY requirements.txt ./

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez votre code source dans l'image Docker
COPY main.py .
COPY templates/ templates/
COPY received_videos/ received_videos/

# Exposez le port sur lequel FastAPI s'exécutera
EXPOSE 80

# Commande pour démarrer votre application
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
