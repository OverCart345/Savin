from fastapi import FastAPI

from api.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(title="Users Service")

    @app.get("/healthz")
    def health_check():
        return {"status": "ok"}

    app.include_router(users_router)

    return app


app = create_app()
