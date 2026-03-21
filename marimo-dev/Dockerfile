# Image officielle de marimo
FROM ghcr.io/marimo-team/marimo:0.19.6-data

# Configuration de l'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
ENV UV_SYSTEM_PYTHON=1
ENV PATH="/code/.venv/bin:$PATH"

# Créer le dossier de travail
WORKDIR /code

# Copier les fichiers projet
COPY pyproject.toml uv.lock ./

# Installer les dépendances
RUN uv sync

# Copier le code
COPY ./scripts/ /code/scripts

CMD ["marimo", "edit", "--no-token", "--host", "0.0.0.0", "-p", "8080"]