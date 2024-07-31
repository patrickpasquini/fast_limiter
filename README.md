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


## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/patrickpasquini/fast_limiter.git
   cd fast_limiter

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt

## Usage

**Create a Fast Limiter**

```python
from fast_limiter import FastLimiter
from fast_limiter.storages import RedisStorage  # or SQLiteStorage
from fastapi import Depends, FastAPI

limiter = FastLimiter(RedisStorage(), limit=5, interval=60) 

app = FastAPI()

@app.get("/limited")
async def limited_endpoint(dependency=Depends(limiter)):
    return {"message": "This endpoint is rate limited"}
```

**Or using decorator**

```python
from fast_limiter import FastLimiter, fast_limit
from fast_limiter.storages import RedisStorage  # or SQLiteStorage
from fastapi import Depends, FastAPI, Request

limiter = FastLimiter(RedisStorage(), limit=5, interval=60) 

app = FastAPI()

@app.get("/limited-decorator")
@fast_limit(limiter)
async def limited_decorator_endpoint(request: Request):
    return {"message": "This endpoint is rate limited with a decorator"}
```