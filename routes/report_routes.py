from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import agent_db, mission_db
import logging
from pathlib import Path

log_path = Path(__file__).parents[1] /"logs"/"app.log"

logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler(log_path)],
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

logger = logging.getLogger()

router = APIRouter()

missions = mission_db.MissionDB()
agents = agent_db.AgentDB()


@router.get("/summary")
def total_report():
        return {"active_agents" : agents.count_active_agents(),
                "total_missions" : missions.count_all_missions(),
                "open_missions" :missions.count_open_missions(),
                "completed_missions" : agents.count_completed_missions(),
                "failed_missions" : agents.count_failed_missions(),
                "critical_missions": missions.count_critical_missions()} 
    


@router.get("/mission-by-status")
def get_mission_by_status():
    return {"NEW": missions.count_by_stats("NEW"),
            "ASSIGNED": missions.count_by_stats("ASSIGNED"),
            "IN_PROGRESS": missions.count_by_stats("IN_PROGRESS"),
             "COMPLETED" : missions.count_by_stats("COMPLETED"),
              "FAILED": missions.count_by_stats("FAILED"),
               "CANCELED"  : missions.count_by_stats("CANCELED")}


@router.get("/top-agent")
def get_top_agent():
    top = missions.get_top_agent()
    return top