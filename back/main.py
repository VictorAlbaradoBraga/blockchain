from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
# Importando os routers
from back.auth import router as auth_router
from back.upload import router as upload_router
from back.productions import router as productions_router
from back.certificate import router as certificate_router

app = FastAPI()


@app.get("/routes")
async def get_routes():
    route_list = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            route_info = {
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name,
            }
            route_list.append(route_info)
    return route_list


# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Primeiro, as rotas da API (backend)
app.include_router(auth_router, prefix="/auth")
app.include_router(upload_router, prefix="/upload")  # Ajuste para "/upload"
app.include_router(productions_router, prefix="/productions")
app.include_router(certificate_router)

# Só depois, servir arquivos estáticos
UPLOAD_DIR = "uploads"
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/src", StaticFiles(directory="front/src"), name="src")
app.mount("/", StaticFiles(directory="front/dist", html=True), name="front")


# Rota principal que serve o index.html
@app.get("/")
async def read_index():
    return FileResponse(Path("front/dist/index.html"))
