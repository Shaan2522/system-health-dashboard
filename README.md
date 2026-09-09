# System Health Dashboard API

A lightweight status API for an operations team, built as part of the C456 SRE Mini Project. It exposes basic health, version, and environment information that engineers and automated monitoring checks can use.

## Prerequisites

- Python 3.9+ (any recent 3.x)
- pip
- Docker Desktop (for containerized run)
- Jenkins (for the CI/CD pipeline) with:
  - Python installed and its full path known
  - Docker Desktop installed, running, and its CLI path known

## Project Structure

```
system-health-dashboard/
├── app.py                  # Flask application (3 endpoints)
├── requirements.txt        # Python dependencies
├── tests/
│   └── test_app.py         # Automated test suite (pytest)
├── Dockerfile               # Container build definition
├── .dockerignore
├── .gitignore
├── Jenkinsfile               # CI/CD pipeline definition
├── MERGE_CONFLICT.md        # Documented merge conflict + resolution
├── TASKS.md                  # Project task list
└── README.md
```

## 1. Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/<your-username>/system-health-dashboard.git
cd system-health-dashboard

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app starts on `http://localhost:5000` using default configuration — no code changes required after install.

### Endpoints

| Endpoint | Description | Example response |
|---|---|---|
| `GET /health` | Basic liveness check | `{"status": "UP"}` |
| `GET /version` | Current app version | `{"version": "v1.1.0"}` |
| `GET /environment` | Current environment, read from `APP_ENV` | `{"environment": "staging"}` |

To set the environment (Windows):
```cmd
set APP_ENV=staging
python app.py
```
(PowerShell: `$env:APP_ENV="staging"`; macOS/Linux: `APP_ENV=staging python app.py`)

If `APP_ENV` is not set, `/environment` defaults to `"development"` so the app still runs cleanly out of the box.

## 2. Run the Tests

```bash
pytest tests/ -v
```

This runs the full suite in one command — 4 tests covering all 3 endpoints, including a check that `/environment` correctly falls back to a default when `APP_ENV` is unset.

## 3. Build & Run with Docker

```bash
# Build a versioned image
docker build -t system-health-dashboard:1.0 .

# Run the container, overriding the environment
docker run -d -p 5000:5000 -e APP_ENV=staging --name health-dashboard system-health-dashboard:1.0

# Verify
curl http://localhost:5000/health
curl http://localhost:5000/version
curl http://localhost:5000/environment

# Clean up
docker stop health-dashboard
docker rm health-dashboard
```

## 4. Jenkins Pipeline

The `Jenkinsfile` defines 6 stages: **Checkout → Install → Test → Build → Tag → Health Check**.

- **Test** runs the full `pytest` suite. If any test fails, the pipeline halts immediately — Build, Tag, and Health Check are all skipped.
- **Tag** appends the Jenkins `%BUILD_NUMBER%` to the image tag (e.g. `system-health-dashboard:9`), so every build produces a traceable, versioned image.
- **Health Check** runs the freshly built image on a temporary port, curls `/health`, and tears the container down afterward regardless of outcome.

### Setting up the pipeline job

1. Install Jenkins and the Docker Pipeline plugin.
2. Create a new **Pipeline** job → set "Pipeline script from SCM" → point it at this repo → Script Path: `Jenkinsfile`.
3. **Note for Windows users:** if `python` or `docker` aren't recognized in the pipeline (common when Jenkins runs as a Windows service with a different PATH than your user account), edit the `environment` block at the top of the `Jenkinsfile` to point `PYTHON` and `DOCKER` at their full paths on your machine, found via:
   ```cmd
   where python
   where docker
   ```
4. Ensure Docker Desktop is running before triggering a build — the daemon must be up for the Build/Tag/Health Check stages to succeed.
5. Click **Build Now**.

## 5. Git Workflow

- `main` — stable, release-ready branch
- `develop` — integration branch
- `feature/*` — one branch per unit of work (health endpoint, tests, Docker, Jenkins, and two branches used to demonstrate a controlled merge conflict)

A real merge conflict was intentionally created and resolved as part of this project — see [`MERGE_CONFLICT.md`](./MERGE_CONFLICT.md) for the full explanation.

A pull request was opened from `develop` into `main`. This project was completed individually, so no peer/facilitator was available for external review; a structured self-review was performed instead on the PR's "Files changed" tab, with comments documenting what was checked (conflict resolution correctness, environment externalization, test coverage).

## 6. AI Assistance Disclosure

Claude (Anthropic) was used throughout this project as a collaborative assistant — helping plan the phased workflow, generate boilerplate (Flask app, tests, Dockerfile, Jenkinsfile), and, importantly, debug several Windows-specific Jenkins issues encountered during pipeline setup (PATH resolution for `python`/`docker` executables, a pip self-upgrade file-lock error, and a non-interactive `timeout` command failure). All generated code was reviewed, tested, and understood before being committed; every fix was validated against actual pipeline runs before being accepted.

## 7. Reflection

**Which Git practice most improved the way I organised my work?**
Working in dedicated feature branches, each tied to one unit of work, made the project's history readable — it's possible to look at the commit graph and understand exactly what changed and why, rather than a single flat sequence of unrelated edits.

**Where did automation detect or prevent an error?**
The Jenkins pipeline caught the intentionally broken version assertion immediately in the Test stage and correctly refused to proceed to Build/Tag/Health Check — demonstrating that a real regression would never make it into a tagged, deployable image.

**What would I change before using this workflow in production?**
I'd move the pipeline off a single developer's local Windows machine and onto a dedicated Jenkins agent/CI runner with a consistent, version-pinned environment, so builds aren't dependent on one machine's local Python/Docker installation paths. I'd also add a linting stage and pin base image digests for reproducibility.

**Which step still depends on manual action, and how could it be automated?**
Triggering the Jenkins build is currently manual ("Build Now"). This could be automated with a GitHub webhook so Jenkins builds automatically on every push to `develop` or on every pull request, giving faster feedback without needing to remember to trigger it.