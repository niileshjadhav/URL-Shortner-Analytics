# URL Shortener with Analytics & Rate Limiting

## Overview
A production-style URL shortener with click analytics and rate limiting — the foundation project demonstrating clean REST API design, caching, and Python backend fundamentals.

## Tech Stack
- Backend: FastAPI, SQLAlchemy
- Database: PostgreSQL
- Cache/Rate-Limiter: Redis

## Key Features
- Custom or auto-generated short codes
- Redirect with click tracking (timestamp, referrer, IP-based approx. location)
- Redis cache-aside pattern for hot URLs
- Token-bucket rate limiting per API key/IP
- Analytics endpoint: clicks over time, top referrers
- Link expiration support

## Architecture Overview

Client --> FastAPI --> Redis (cache + rate limit) --> PostgreSQL (persistent store)

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d   # postgres + redis
alembic upgrade head
uvicorn app.main:app --reload
```

## Interview Talking Points
- Token bucket vs sliding window rate limiting
- Cache invalidation on link update/expiry
- Handling race conditions on short-code generation
- Read-heavy optimization via Redis cache-aside

url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entrypoint, middleware, router registration
│   ├── config.py                # Settings (env vars, DB/Redis URLs, rate-limit config)
│   ├── dependencies.py          # Shared deps: get_db, get_redis, get_api_key, rate_limiter
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── links.py         # POST /links (create short URL), GET/PATCH/DELETE /links/{code}
│   │   │   ├── redirect.py      # GET /{short_code} — the actual redirect endpoint
│   │   │   └── analytics.py     # GET /links/{code}/analytics, /clicks, /referrers
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── link.py               # SQLAlchemy model: Link (code, target_url, expires_at, owner)
│   │   └── click_event.py        # SQLAlchemy model: ClickEvent (link_id, ts, referrer, ip, geo)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── link.py               # Pydantic: LinkCreate, LinkResponse, LinkUpdate
│   │   └── analytics.py          # Pydantic: ClicksOverTime, TopReferrers
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── shortener.py          # short-code generation (base62 + collision retry / Snowflake ID)
│   │   ├── cache.py               # Redis cache-aside: get_link, set_link, invalidate_link
│   │   ├── rate_limiter.py        # Token-bucket implementation (Redis Lua script or INCR+EXPIRE)
│   │   └── analytics.py           # Aggregation queries for the analytics endpoints
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py             # SQLAlchemy engine + session factory
│   │   └── base.py                # Declarative base, shared mixins (timestamps, UUID PK)
│   │
│   └── core/
│       ├── __init__.py
│       ├── security.py            # API key validation / hashing
│       └── logging.py             # Structured logging config
│
├── alembic/
│   ├── env.py
│   └── versions/                  # Migration scripts (create links, click_events tables)
├── alembic.ini
│
├── tests/
│   ├── conftest.py                # Test DB/Redis fixtures (testcontainers or fakeredis)
│   ├── test_shortener.py          # Collision handling, code generation
│   ├── test_rate_limiter.py       # Token bucket edge cases
│   ├── test_redirect.py           # Cache hit/miss, expiry behavior
│   └── test_analytics.py
│
├── scripts/
│   └── seed_data.py                # Populate sample links/clicks for local testing
│
├── docker-compose.yml               # postgres + redis services
├── Dockerfile
├── requirements.txt
├── .env.example
├── README.md
└── pyproject.toml / setup.cfg       # (optional, if you lint with ruff/black)
