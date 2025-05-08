from fastapi import FastAPI
from routers import get_routes, post_routes, put_routes, delete_routes

app = FastAPI()

app.include_router(get_routes.router)
app.include_router(post_routes.router)
app.include_router(put_routes.router)
app.include_router(delete_routes.router)