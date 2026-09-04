from fastapi import FastAPI

app = FastAPI(
    title="FutbolX Media Server",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "name": "FutbolX Media Server",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/api/streams")
def streams():
    return {
        "streams": []
    }
