from fastapi import FastAPI
import uvicorn

from api.router import all_routers


app = FastAPI(
    title="Simplified analog of Jira/Asana"
)


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
