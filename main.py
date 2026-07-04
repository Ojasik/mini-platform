from fastapi import FastAPI
import socket, os, redis

app = FastAPI()


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
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
        return {"visits": value}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/ready")
def ready():
    try:
        client = get_redis()
        client.ping()
        return {"status": "ready"}
    except:
        return {"status": "not ready"}, 503
