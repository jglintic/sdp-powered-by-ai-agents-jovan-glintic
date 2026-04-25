# 🚀 Mars Rover Kata — TDD/BDD Multi-Agent System

A software engineering kata that simulates a Mars Rover navigating a grid using movement and rotation commands, implemented using **strict Test-Driven Development (TDD)** and **Behavior-Driven Development (BDD)** with AI-assisted agents.

---

## 📖 Project Description

The Mars Rover kata models a rover exploring a rectangular grid based on a sequence of commands. The system processes movement and rotation instructions while ensuring correct positioning, obstacle handling, and grid wrapping.

Key features include:
- Movement and rotation (N, S, E, W)
- Command parsing and execution
- Toroidal grid wrapping (edge-to-edge movement)
- Obstacle detection with safe stopping

The project demonstrates **clean architecture**, **Domain-Driven Design (DDD)**, and **incremental development using RED-GREEN-REFACTOR cycles**.

---

## 🎯 What This Kata Solves

- Enforces **strict TDD discipline**
- Demonstrates **BDD scenario-based development**
- Applies **arc42 architecture documentation**
- Uses **C4 model diagrams** for system design
- Implements **CI/CD pipelines with Docker**
- Showcases **AI-assisted development with Kiro CLI agents**

---

## 🧱 Tech Stack

- **Python 3.12**
- **pytest** — testing framework
- **Docker** — isolated test execution
- **PlantUML (C4 model)** — architecture diagrams
- **Sphinx** — documentation generation
- **GitHub Actions** — CI/CD automation

---

## 🏗️ Architecture Overview

The system is designed using **arc42** and **C4 model** principles.

### Main Domains (DDD)
- Rover Control
- Command Processing
- Grid/Map
- Simulation Orchestration
- Output Handling

📂 Architecture documentation:
https://github.com/jglintic/sdp-powered-by-ai-agents-jovan-glintic/tree/master/architecture

📘 Live Sphinx documentation:
https://jglintic.github.io/

---

## ▶️ How to Build and Run (Docker)

Build the Docker image and run the tests:
```bash
docker build -t mars-rover .
docker run --rm mars-rover
```

---

## Project structure:
```
  sdp-powered-by-ai-agents-jovan-glintic/
  ├── .github/
  │   └── workflows/
  │       ├── ci.yml
  │       └── docs-deploy.yml
  ├── .kiro/
  │   └── agents/
  │       ├── architecture-agent.json
  │       ├── cicd-agent.json
  │       ├── git-agent.json
  │       ├── requirements-agent.json
  │       ├── tdd-bdd-agent.json
  │       └── tdd-bdd-prompt.md
  ├── docs/
  │   ├── architecture/
  │   │   ├── 01-introduction-and-goals.md
  │   │   ├── 02-constraints.md
  │   │   ├── 03-system-scope-and-context.md
  │   │   ├── 04-solution-strategy.md
  │   │   ├── 05-building-block-view.md
  │   │   ├── 06-runtime-view.md
  │   │   ├── 07-deployment-view.md
  │   │   ├── 08-crosscutting-concepts.md
  │   │   ├── 09-architecture-decisions.md
  │   │   ├── 10-quality-requirements.md
  │   │   ├── 11-risks-and-technical-debts.md
  │   │   ├── 12-glossary.md
  │   │   └── diagrams/
  │   │       ├── c4-component.puml / .svg
  │   │       ├── c4-container.puml / .svg
  │   │       ├── c4-context.puml / .svg
  │   │       ├── deployment.puml / .svg
  │   │       ├── seq-happy-path.puml / .svg
  │   │       └── seq-obstacle.puml / .svg
  │   ├── user-stories/
  │   │   ├── command-processing.md
  │   │   ├── grid-map.md
  │   │   ├── rover-control.md
  │   │   └── README.md
  │   ├── conf.py
  │   ├── docs-deploy.yml
  │   ├── index.rst
  │   ├── Makefile
  │   └── requirements.txt
  ├── scripts/
  │   ├── hooks/
  │   │   ├── check-commit-msg.sh
  │   │   ├── docker-test.sh
  │   │   └── validate-plantuml.sh
  │   └── generate-plantuml.sh
  ├── src/
  │   └── mars_rover/
  │       ├── __init__.py
  │       ├── __main__.py
  │       ├── domain.py
  │       └── input_parser.py
  ├── tests/
  │   └── test_rover.py
  ├── Dockerfile
  ├── LICENSE
  ├── README.md
  ├── .pre-commit-config.yaml
  └── pyproject.toml
```

---

## 🤖 Development Approach

This project is built using a multi-agent workflow:
- Requirements Agent → derives user stories (DDD + Pareto)
- Architecture Agent → generates arc42 documentation
- CI/CD Agent → creates Docker + GitHub Actions pipeline
- TDD/BDD Agent → implements features one test at a time

---

## 👤 Author

Jovan Glintic

GitHub: https://github.com/jglintic
Project repository:
https://github.com/jglintic/sdp-powered-by-ai-agents-jovan-glintic
