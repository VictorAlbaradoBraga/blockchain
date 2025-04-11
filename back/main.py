from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Serve os arquivos estáticos da pasta 'front'
app.mount("/static", StaticFiles(directory="front"), name="static")

# Quando acessar "/", manda o index.html
@app.get("/")
async def read_index():
    return FileResponse(Path("front/index.html"))
