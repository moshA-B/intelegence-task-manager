from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
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

class Agent(BaseModel):
    name : str
    specialty  :str | None = None
    agent_rank : Literal['Junior','Senior','Commander']

class UpdateAgent(BaseModel):
    name : str | None = None
    specialty  :str | None = None
    is_active : bool | None = None
    agent_rank : Literal['Junior','Senior','Commander'] | None = None


router = APIRouter()

agents = agent_db.AgentDB()



@router.post("",status_code=201)
def create_agent(body : Agent):
    logger.info("POST agent called")
    logger.info("creating agent")
    new = handel_content(agents.create_agent(body.model_dump(exclude_none=True)), "failed to create agent")
    logger.info("agent created %s", new["id"])
    return new
    


@router.get("")
def get_all_agents():
    logger.info("GET all  agent called ")
    logger.info("initiating ...")
    all = handel_content(agents.get_all_agents(), "no agents yet")
    logger.info("GET all agents successful")
    return all

@router.get("/{id}")
def get_agent_by_id(id : int):
    logger.info("GET agent by id called ")
    logger.info("initiating ...")
    agent = handel_content(agents.get_agent_by_id(id), f"agent {id} not found")
    logger.info("agent found %s", id)
    return agent


@router.put("/{id}",status_code=201)
def update_agent(id : int, body: UpdateAgent):
    logger.info("update agent called")
    logger.info("updating agent...")
    handel_content(agents.update_agent(id, body.model_dump(exclude_none=True)), "id not found")
    logger.info("agent %s updated", id)
    return {"message": "updated"}



@router.put("/{id}/deactivate",status_code=201)
def deactivate_agent(id):
    logger.info("deactivate agent called")
    logger.info("deactivating agent...")
    handel_content(agents.deactivate_agent(id), "id not found")
    logger.info("agent %s is deactivated", id)
    return {"message": "deactivated"}

@router.get("{id}/performance",status_code=201)
def get_performance(id: int):
    logger.info("agent performance called")
    logger.info("showing agent performance...")
    performance = handel_content(agents.get_agent_performance(id), "id not found")
    logger.info("got performance for agent %s", id)
    return performance

