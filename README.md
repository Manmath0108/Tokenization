# Tokenization Project — README

This repository contains a small word-level tokenizer API implemented in FastAPI, packaged with Docker, and deployed to Render. It is designed as a learning project to teach tokenization fundamentals and the full ML engineering lifecycle (notebook → script → API → Docker → cloud). Follow the instructions below to run, test, and deploy the project.

---

## Quick links (what you need)

* Local app (dev): `uvicorn APIs.tokenizer_api:app --reload`
* Production Dockerfile: `Dockerfile.prod`
* Docker Hub image (example): `manmath0108/tokenizer-api:prod`

---

## Repository layout

```
Tokenization/
├── APIs/
│   └── tokenizer_api.py        # FastAPI app (health, version, tokenize)
├── PythonScripts/
│   ├── word_level_tokenizer.py # tokenizer functions
│   ├── unkown_words_tokenizer.py
│   └── multiple_word_level_tokenizer.py
├── JupyterNotebooks/           # Notebooks used during development
├── Dockerfile                  # dev Dockerfile
├── Dockerfile.prod             # production Dockerfile (non-root)
├── requirements.txt            # Python deps
├── tests/                      # pytest tests
└── README.md                   # this file
```

---

## Prerequisites

* Linux / macOS / Windows WSL
* Git
* Conda (Miniconda / Anaconda) or Python 3.10+ environment
* Docker (daemon running)
* (Optional) Docker Hub account and Render account for deployment

---

## 1 — Create and use the conda environment (recommended)

```bash
# create env (example name nlp_env)
conda create -n nlp_env python=3.11 -y
conda activate nlp_env

# install pip requirements
pip install -r requirements.txt
```

> If you prefer venv: `python -m venv .venv && source .venv/bin/activate` then `pip install -r requirements.txt`.

---

## 2 — Run the app locally (development)

Run the FastAPI app directly (fast iteration):

```bash
# from repo root
uvicorn APIs.tokenizer_api:app --reload
```

Open interactive docs at: `http://127.0.0.1:8000/docs`

Test endpoints (examples):

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/version
curl -s -X POST http://127.0.0.1:8000/tokenize -H "Content-Type: application/json" -d '{"sentence":"I enjoy AI"}'
```

---

## 3 — Build production Docker image

Production Dockerfile is `Dockerfile.prod` (non-root, minimal). To build:

```bash
# build image
docker build -f Dockerfile.prod -t tokenizer-api:prod .

# run image locally (safe resource limits recommended)
docker run --rm -p 8000:8000 --name tokenizer-api-prod --memory="512m" --cpus="1.0" tokenizer-api:prod
```

Then test the endpoints against `http://127.0.0.1:8000` as above.

---

## 4 — Publish to Docker Hub (example)

1. Create a Docker Hub account ([https://hub.docker.com](https://hub.docker.com)). 2. Create an access token (recommended) in Hub → Account Settings → Security.

Tag and push (replace `<DOCKERHUB_USER>` with your username):

```bash
# tag
docker tag tokenizer-api:prod <DOCKERHUB_USER>/tokenizer-api:prod

# push (login first or use token)
docker login --username <DOCKERHUB_USER>
docker push <DOCKERHUB_USER>/tokenizer-api:prod
```

*Tip:* if your local credential helper requires setup, you can use a temporary docker config as shown in development notes to avoid `pass` issues.

---

## 5 — Deploy on Render (Docker image)

1. Create Render account [https://dashboard.render.com](https://dashboard.render.com)
2. New → Web Service → choose **Docker** and enter: `docker.io/<DOCKERHUB_USER>/tokenizer-api:prod`
3. Set port `8000` and create service.
4. Render will pull the image and run it; use the provided public URL to test the endpoints.

---

## API Reference (endpoints)

* `GET /health` → `{ "status": "ok" }` (simple readiness)
* `GET /version` → `{ service, version, python, cwd }` (debug info)
* `POST /tokenize` → body `{ "sentence": "..." }`

  * Response: `{ input_sentence, encoded, decoded, vocab_size }`

---

## Testing

Run pytest (project root):

```bash
PYTHONPATH=. pytest -q
```

Tests cover basic tokenizer functions. If tests fail, read the failure lines and inspect `PythonScripts/` functions.

---

## Troubleshooting & tips

* **Docker permission denied**: If `docker` complains `permission denied` on `/var/run/docker.sock`, add user to docker group:

  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

  Log out/in if needed.

* **`pass not initialized` on `docker login`**: Use a temporary docker config or login via web-based flow; or initialize `pass` (not necessary).

* **Chrome / ChatGPT UI problems**: Use Incognito or disable extensions if the web UI becomes unresponsive.

* **Port in use**: If port 8000 is busy, map to another host port: `-p 8080:8000` and test on `http://127.0.0.1:8080`.

---

## Security note (important)

If you created a Docker Hub token during this process and pasted it somewhere, **revoke it immediately** and create a fresh token. Treat tokens like passwords.

---

## CI automation (optional)

Add a GitHub Actions workflow (`.github/workflows/publish-dockerhub.yml`) to build and push `Dockerfile.prod` on `main` pushes. Store `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` in GitHub Secrets.

---

## License

This project is provided under the MIT License (see `LICENSE` file).

---

If you want, I can also create a short `README.md` snippet that includes sample `curl` calls ready to copy — or I can create a full `README.md` file in the repo for you. Which would you prefer?
