# AppNest

AppNest is a modular full-stack platform that combines **games, productivity tools, and social features** into a unified interactive environment.
It uses a **FastAPI backend**, **React + Vite frontend**, and a **dynamic module execution system** that allows tools and games to run as pluggable modules.

---

# Architecture Overview

AppNest follows a layered backend architecture to keep responsibilities separated.

```
backend/
 ├ api/            # FastAPI route handlers
 ├ core/           # Configuration, database, security, caching
 ├ domain/         # Pure business logic (XP rules, profile logic, etc.)
 ├ repositories/   # Database interaction layer
 ├ services/       # Application logic & orchestration
 ├ models/         # SQLAlchemy models
 ├ modules/        # Game and tool modules
 ├ platform/       # Module registry and executor system
```

Flow of request handling:

```
API Route
   ↓
Service Layer
   ↓
Domain Logic
   ↓
Repository Layer
   ↓
Database
```

---

# Features

### Platform

* Modular runtime system
* Dynamic module execution
* XP and progression system
* Leaderboards
* Notifications
* Admin analytics

### Games

* Snake
* Flappy Bird
* Tic Tac Toe
* Brick Breaker

### Tools

* BMI Calculator
* Age Calculator
* CGPA Calculator
* Currency Converter
* Unit Converter
* Translator
* Weather Tool
* Joke Generator
* Zodiac (Rashi) Generator

### Social & Profile

* User profiles
* Achievements
* XP progression
* Quests
* Leaderboards

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Redis
* JWT Authentication

## Frontend

* React
* Vite
* TailwindCSS
* Zustand state management

## Infrastructure

* Docker
* Docker Compose

---

# Project Structure

```
AppNest
│
├ backend
│   ├ app
│   │   ├ api
│   │   ├ core
│   │   ├ domain
│   │   ├ repositories
│   │   ├ services
│   │   ├ models
│   │   ├ modules
│   │   └ platform
│
├ frontend
│   ├ src
│   │   ├ api
│   │   ├ components
│   │   ├ modules
│   │   ├ realms
│   │   ├ store
│   │   └ engine
│
└ docker-compose.yml
```

---

# Running the Project

## Using Docker (Recommended)

```bash
docker-compose up --build
```

Services started:

* Backend API
* Frontend UI
* Redis
* Database

---

# Backend Development

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

Run migrations:

```bash
alembic upgrade head
```

Seed data:

```bash
python scripts/seed_modules.py
```

---

# Frontend Development

Install dependencies:

```bash
cd frontend
npm install
```

Run development server:

```bash
npm run dev
```

---

# Module System

Modules are dynamically registered and executed through the **Module Registry**.

```
module request
      ↓
module registry
      ↓
module executor
      ↓
tool/game module
```

Modules live in:

```
backend/app/modules/
```

Categories:

```
modules/games
modules/tools
```

Each module implements a standard executor interface.

---

# Testing

Backend tests:

```bash
pytest backend/tests
```

---

# Future Improvements

* Plugin marketplace for modules
* Real-time multiplayer games
* AI assistant integrations
* Advanced analytics dashboard
* Microservice architecture split

---

# License

This project is open-source and available under the MIT License.
