from fastapi import FastAPI
import socket, os, redis, time

app = FastAPI()

def wait_for_redis():
    for i in range(10):
        try:
            r = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
            )
            r.ping()
            print("Redis is ready")
            return r
        except:
            print("Waiting for Redis...")
            time.sleep(1)

    raise Exception("Redis not available")

redis_client = wait_for_redis()

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
def redis():
    redis_client.incr("visits")
    return {"visits": redis_client.get("visits").decode()}
