# Image officielle de Python (choisir une version précise, pas "latest")
FROM python:3.12.3 

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
ENV UV_SYSTEM_PYTHON=1

# Créer le dossier de travail
WORKDIR /code

# Copier les fichiers projet
COPY pyproject.toml uv.lock ./

# Installer les dépendances
RUN uv sync

# Copier le code
COPY ./scripts/ /code/

# Commande par défaut (modifiable)
CMD ["python"]