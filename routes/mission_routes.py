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
def create_mission():
    pass

@router.get("")
def get_all_missions():
    pass

@router.get("/{id}")
def get_mission_by_id(id: int):
    pass


@router.put("/{id}/assign/{agent_id} ")
def assign_mission_to_agent(id : int, agent_id : int):
    pass

@router.put("/{id}/start")
def start_mission(id : int):
    pass

@router.put("/{id}/complete")
def complete_mission(id: int):
    pass

@router.put("/{id}/fail")
def fail_mission(id :int):
    pass

@router.put("/{id}/cancel")
def cancel_mission(id :int):
    pass

