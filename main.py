from fastapi import FastAPI
import socket, os, redis

app = FastAPI()


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        decode_responses=True,
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "service": "mini-platform",
        "version": "0.1",
        "hostname": socket.gethostname()
    }

@app.get("/redis")
def redis_endpoint():
    client = get_redis()

    try:
        client.incr("visits")
        value = client.get("visits")
        return {"visits": value.decode()}
    except Exception as e:
        return {"error": "redis unavailable"}
