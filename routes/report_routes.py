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


@router.get("/summary")
def total_report():
    pass

@router.get("/mission-by-status")
def get_mission_by_status():
    pass


@router.get("/top-agent")
def get_top_agent():
    pass