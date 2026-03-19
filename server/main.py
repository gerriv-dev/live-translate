from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from upstash_redis.asyncio import Redis

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
redis = Redis.from_env()


@app.get("/")
async def index():
    return FileResponse("./static/index.html")


@app.post("/server-ip")
async def set_server_ip(ip: str = Form()):
    await redis.set("server-ip", ip)
    return {"ip": ip}


@app.get("/server-ip")
async def get_server_ip():
    return {"ip": await redis.get("server-ip")}
