# Fast Limiter

This is a rate limiting solution designed for FastAPI applications.
The project demonstrates the implementation of rate limiting using different storage options.

## Overview

`Fast Limiter` showcases how to implement rate limiting in a FastAPI application.
It includes support for Redis and SQLite as storage backends, allowing you to control how frequently clients can access your API endpoints.

## Features

- **Rate Limiting**: Controls the rate at which clients can make requests.
- **Redis Storage**: Scalable, fast, and suitable for production.
- **SQLite Storage**: Simple and file-based, ideal for testing and development.

### Prerequisites

- Python 3.11+
- Redis (if using Redis for storage)
- SQLite (if using SQLite for storage)

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/patrickpasquini/fast_limiter.git
   cd fast_limiter

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt

3. **Set up the environment variables**:

    Create a `.env` file in the root directory of the project with the following content:

    ```env
    REDIS_URL=redis://localhost
    DB_PATH=rtl.db
    ```

    The `REDIS_URL` and `DB_PATH` variables can be customized to point to your specific Redis instance or SQLite database file.

## Usage

**Create a Fast Limiter**

```python
from fast_limiter import FastLimiter
from fast_limiter.storages import RedisStorage  # or SQLiteStorage
from fastapi import Depends, FastAPI

limiter = FastLimiter(RedisStorage(), limit=5, interval=60) 

app = FastAPI()

@app.get("/limited", dependencies=[Depends(limiter)])
async def limited_endpoint():
    return {"message": "This endpoint is rate limited"}
```

**Or using decorator**

```python
from fast_limiter import FastLimiter, fast_limit
from fast_limiter.storages import RedisStorage  # or SQLiteStorage
from fastapi import FastAPI, Request

limiter = FastLimiter(RedisStorage(), limit=5, interval=60) 

app = FastAPI()

@app.get("/limited-decorator")
@fast_limit(limiter)
async def limited_decorator_endpoint(request: Request):
    return {"message": "This endpoint is rate limited with a decorator"}
```