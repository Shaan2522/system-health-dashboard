# Task List — System Health Dashboard API

## 1. Application
- [ ] `/health` endpoint → `{"status": "UP"}`
- [ ] `/version` endpoint → returns app version
- [ ] `/environment` endpoint → reads env var, not hardcoded
- [ ] Manual verification of all endpoints locally

## 2. Testing
- [ ] Test for `/health`
- [ ] Test for `/version`
- [ ] Test for `/environment`
- [ ] Single command to run full suite (`pytest`)
- [ ] Demonstrate one intentional test failure, then restore

## 3. Git Workflow
- [ ] `main` and `develop` branches created
- [ ] `feature/health-endpoint` branch
- [ ] `feature/add-tests` branch
- [ ] Controlled merge conflict created and resolved (documented)
- [ ] PR opened from `develop` → `main`
- [ ] Review requested and addressed

## 4. Containerization
- [ ] `Dockerfile`
- [ ] `.dockerignore`
- [ ] Build versioned image
- [ ] Run container with env var override
- [ ] Verify endpoints against running container

## 5. Jenkins Pipeline
- [ ] Checkout stage
- [ ] Install stage
- [ ] Test stage
- [ ] Build stage
- [ ] Tag stage (build number)
- [ ] Health-check stage
- [ ] Confirm pipeline halts on failed test
- [ ] Capture screenshot of successful run

## 6. Documentation
- [ ] README with setup/run/test/docker/verify instructions
- [ ] Merge-conflict explanation
- [ ] Reflection questions answered