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

def handel_content(func, fail_message = "", status_code = 404):
    if not func:
        logger.error(fail_message)
        raise HTTPException(status_code=status_code, detail=fail_message)
    else:
        return func



class Mission(BaseModel):
    title : str
    description : str
    location : str
    difficulty : int
    importance : int


missions = mission_db.MissionDB()
agents = agent_db.AgentDB()

router = APIRouter()


@router.post("")
def create_mission(body : Mission):
    logger.info("POST new mission called")
    logger.info("creating new mission ")

    new = handel_content(missions.create_mission(body.model_dump(exclude_none=True)), "failed to create mission", 500)
    logger.info("new mission added")
    
    return new

@router.get("")
def get_all_missions():
    logger.info("get all missions called")
    logger.info("initiating")

    all_missions = handel_content(missions.get_all_missions(), "no missions yet")
    logger.info("get all missions successful")
    return all_missions
    

@router.get("/{id}")
def get_mission_by_id(id: int):
    logger.info("GET agent by id called")
    logger.info("initiating")

    mission = handel_content(missions.get_mission_by_id(id), f"id not found {id}")
    logger.info("agent found %s", id)
    return mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id : int, agent_id : int):
    logger.info("assigned mission called")
    logger.info("initiating")

    mission = handel_content(get_mission_by_id(id), "mission doesn't exist")

    agent = handel_content(agents.get_agent_by_id(agent_id), "agent doesn't exist")

    if not agent["is_active"]:
        logger.error("agent no active ")
        raise HTTPException(status_code=400, detail="agent not active")
    
    if not mission["status"] == "NEW":
        logger.error("requested mission was already assigned")
        raise HTTPException(status_code=400, detail="mission already assigned")

    if mission["risk_level"] == "CRITICAL": 
        if agent["agent_rank"] != "Commander":
            logger.error("agent is not ranked to handel mission")
            raise HTTPException(status_code=400, detail="agent not ranked for this mission")
    
    handel_content(missions.assign_missions(id, agent_id), "failed to assign mission")
    logger.info("assigned mission successfully")
    return {"massage" :"assigned"}
        
    

@router.put("/{id}/start")
def start_mission(id : int):
    logger.info("start mission called to start mission %s", id)

    mission = handel_content(get_mission_by_id(id), "mission not found")
    if mission["status"] != "ASSIGNED":
        logger.error("mission %s already started", id)
        raise HTTPException(status_code=400, detail="mission already started")
    
    if not mission["assigned_agent_id"]:
        logger.error("mission was not yet assigned")
        raise HTTPException(status_code=400, detail="mission was not yet assigned" )
    
    
    handel_content(missions.update_mission_status(id, "IN_PROGRESS"), "failed to start mission", 500)
    logger.info("started mission %s", id)
    return {"message": "started"}


@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info("complete mission called to complete mission %s", id)

    mission = handel_content(get_mission_by_id(id), "mission not found")
    if mission["status"] != "IN_PROGRESS":
        logger.error("mission %s has not yet started", id)
        raise HTTPException(status_code=400, detail="mission hasn't started")
    
    handel_content(missions.update_mission_status(id, "COMPLETED"), "failed to complete mission", 500)
    logger.info("completed mission %s", id)
    agents.increment_completed(mission["assigned_agent_id"])
    return {"massage" :"completed"}


@router.put("/{id}/fail")
def fail_mission(id :int):
    logger.info("fail mission called to fail mission %s", id)

    mission = handel_content(get_mission_by_id(id), "mission not found")
    if mission["status"] != "IN_PROGRESS":
        logger.error("mission %s has not yet started", id)
        raise HTTPException(status_code=400, detail="mission hasn't started")
    
    handel_content(missions.update_mission_status(id, "FAILED"), "failed to complete mission", 500)
    logger.info("mission %s failed", id)
    agents.increment_failed(mission["assigned_agent_id"])
    return {"massage" :"marked as failed"}


@router.put("/{id}/cancel")
def cancel_mission(id :int):
    logger.info("cancel mission called to cancel mission %s", id)

    mission = handel_content(get_mission_by_id(id), "mission not found")
    if mission["status"] not in ["IN_PROGRESS", "NEW"]:
        logger.error("can not cancel completed missions", id)
        raise HTTPException(status_code=400, detail="can not cancel completed missions")
    
    handel_content(missions.update_mission_status(id, "CANCELED"), "failed to cancel mission", 500)
    logger.info("mission %s has been aborted", id)
    return {"massage" :"canceled"}

