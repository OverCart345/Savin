from fastapi import FastAPI

from api.users import router as users_router
from api.articles import router as articles_router
from api.comments import router as comments_router


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/healthz")
    def health_check():
        return {"status": "ok"}

    app.include_router(users_router)
    app.include_router(articles_router)
    app.include_router(comments_router)

    return app


app = create_app()
