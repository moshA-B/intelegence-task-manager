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

@router.post("")
def create_agent():
    pass


@router.get("")
def get_all_agents():
    pass

@router.get("/{id}")
def get_agent_by_id(id : int):
    pass


@router.put("/{id}")
def update_agent(id : int, body):
    pass

@router.put("/{id}/deactivate")
def deactivate_agent():
    pass

@router.get("{id}/performance")
def get_performance(id: int):
    pass

