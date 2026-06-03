# JobQ

JobQ is a UCC CK401 Year 3 college project built to demonstrate practical CI/CD and DevOps principles through a compact but realistic distributed system. It is intentionally split into independent services so the project can show how modern applications are built, tested, containerized, deployed, and operated when several moving parts need to work together. 🚀

At its core, JobQ is an asynchronous job-processing API. A client submits text to the FastAPI application, the API stores a new job record in PostgreSQL, and a Celery worker consumes the queued task through Redis and processes it in the background. That separation is central to the project: the API remains responsive while work is delegated to a worker process, modelling the kind of loosely coupled architecture used in real production systems. ⚙️

## 🎓 Academic Purpose

This repository was developed as a UCC CK401 Year 3 project to demonstrate:

- containerized application design
- service separation and orchestration
- asynchronous background processing
- health checking and operational visibility
- CI validation with meaningful automated tests
- automated deployment to a hosted AWS environment

The aim is not only to build an API, but to show the full operational pipeline around that API: code is pushed, CI runs automatically, tests validate the build, and successful changes are deployed to a live server.

## 🧠 Human Design and AI Use

Generative AI was used during development as an implementation aid for coding, iteration, and documentation support. However, the system design, architecture, project goals, and engineering decisions were human-designed and human-directed.

In other words, AI assisted with parts of the build process, but the structure of the system and the DevOps pipeline were deliberately planned by a person rather than generated as a fully automated solution.

## 🏗️ Architecture Overview

The project is composed of four main services defined in Docker Compose:

- `api`: a FastAPI application that exposes the HTTP endpoints
- `worker`: a Celery worker that processes jobs asynchronously
- `db`: a PostgreSQL database that stores submitted jobs and their results
- `redis`: a Redis instance used as the Celery broker and result backend

This layout is deliberate. Each container has a distinct responsibility, which makes the interplay between networking, service dependencies, health checks, and deployment easier to understand. It also reflects the kind of separation commonly found in DevOps-oriented systems, where application concerns, messaging, data persistence, and background work are isolated but coordinated. 🐳

## 🗺️ Architecture Diagram

```mermaid
flowchart LR
		U[Client] -->|POST /jobs| API[FastAPI API Container]
		U -->|GET /jobs/{id}| API
		U -->|GET /health| API

		API -->|store job + status| DB[(PostgreSQL)]
		API -->|queue task| R[(Redis)]
		R -->|deliver task| W[Celery Worker Container]
		W -->|read/update job| DB

		GH[GitHub Actions CI] -->|tests pass| DEPLOY[Deploy Workflow]
		DEPLOY -->|SSH + docker-compose up --build| AWS[AWS EC2 Host]
		AWS --> API
		AWS --> W
		AWS --> DB
		AWS --> R
```

## 🔄 How It Works

1. A client sends a request to `POST /jobs` with some text.
2. The API creates a new database record with a `pending` status.
3. The API queues a Celery task through Redis.
4. The worker picks up that task and processes it asynchronously.
5. The worker updates the job status and stores the result in PostgreSQL.
6. The client can query `GET /jobs/{job_id}` to check whether the job has completed.

There is also a lightweight health endpoint at `GET /health`, used both for operational checks and container health monitoring. ❤️

## 🧪 DevOps and CI/CD Focus

JobQ is designed to demonstrate the DevOps lifecycle around a small service-based system.

- the application is containerized with separate Dockerfiles for the API and worker
- Docker Compose brings the full stack up as a coordinated multi-container environment
- GitHub Actions runs CI on pushes and pull requests targeting `main`
- the CI pipeline now runs a real `pytest` suite rather than a dummy import check
- the test suite covers the health endpoint, job submission, job retrieval, and worker-side processing logic
- a deployment workflow is triggered after the CI workflow completes successfully
- the deployment job connects to an AWS EC2 instance over SSH, pulls the latest code, and rebuilds the running containers

This means the repository demonstrates more than local development. It shows how code moves from source control to validation to automated deployment in a hosted environment. 🔁

## ✅ Current Test Coverage

The automated test suite is intentionally small but meaningful. It currently verifies:

- the `/health` endpoint returns a valid status response
- submitting a job through `/jobs` persists the request and queues background work
- fetching a job by ID returns the stored job state
- the worker task updates the job status and writes the processed result

These tests make the CI pipeline more representative of the actual system behavior, rather than only proving that the code imports successfully. 🛠️

## ☁️ Live Deployment

The project is hosted on AWS and automatically deployed after a successful push-and-test pipeline.

Health endpoint:

- http://56.228.23.51:8000/health

If deployment is healthy, that endpoint returns:

```json
{"status": "ok"}
```

## 📦 Why The Project Uses Containers

Containerization is central to the purpose of the project. Running the API, worker, database, and Redis in separate containers makes the operational model visible:

- each component can be built and restarted independently
- dependencies between services are explicit
- the application behaves more like a real deployment target
- infrastructure concerns such as ports, environment variables, restart policies, and health checks become part of the design

For a DevOps demonstration, this is much more useful than a single-process application because it makes the coordination between independent services visible and testable. 🐋

## 💻 Local Development

Create a local environment file from the checked-in template:

```bash
cp .env.example .env
```

The `.env.example` file contains the non-secret configuration shape expected by the application and is also used by GitHub Actions to recreate `.env` during CI. That keeps local development and CI aligned around the same environment-variable structure. 🔐

Start the full stack with Docker Compose:

```bash
docker-compose up -d --build
```

Then test the API:

```bash
curl http://localhost:8000/health
```

Create a job:

```bash
curl -X POST http://localhost:8000/jobs \
	-H "Content-Type: application/json" \
	-d '{"text":"Hello JobQ"}'
```

Check a job result:

```bash
curl http://localhost:8000/jobs/1
```

Run the automated tests locally:

```bash
source venv/bin/activate
python -m pytest
```

## 📝 Summary

JobQ is a compact distributed system built for academic demonstration. It combines FastAPI, Celery, Redis, PostgreSQL, Docker, GitHub Actions, automated testing, and AWS deployment into one project so the relationship between application code, background processing, containers, CI/CD, and live operations is clear and testable. ✨
