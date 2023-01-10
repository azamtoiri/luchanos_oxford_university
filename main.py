import uvicorn

from typing import cast

from fastapi import FastAPI
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from api.handlers import user_router
from db.session import async_session, engine
from db.models import Base


async def _init_database() -> AsyncSession:
    """Try to connect to the database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except ConnectionRefusedError:
        print ("Database connection failed")
    else:
        print("Database connection established")
        
    return cast(AsyncSession, async_session())



# region: API ROUTES

# create instance of the app
app = FastAPI(title="luchanos-oxford-university")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

@app.on_event("startup")
async def startup() -> None:
    """Perform initial setup and establish connections/sessions."""
    print("API Server starting...")
    app.state.db_session = _init_database()
    

@app.on_event("shutdown")
async def shutdown() -> None:
    """Close the connections/sessions."""
    print("API Server stopping...")
    await engine.dispose()
    await app.state.db_session.close()

# endregion

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
