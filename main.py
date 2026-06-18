from fastapi import FastAPI
import uvicorn
from routes import mission_routes,agent_routes, report_routes
from database import db_connection


app = FastAPI()
app.include_router(mission_routes.router, prefix="/missions", tags =["missions"])
app.include_router(agent_routes.router, prefix="/agents", tags=["agents"])
app.include_router(report_routes.router, prefix="/reports", tags=["reports"])

db_connection.DB_connection.create_database()
db_connection.DB_connection.create_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)