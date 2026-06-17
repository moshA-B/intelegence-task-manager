# Intelligence Task Manager

a system for handling tasks and assigning them to agents




## Folder structure:

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Table structure:

### Agents:

|column|type|info|
|----|----|----|
|id|INT, AUTO_INCREMENT, PRIMARY KEY|unique id|
|name|VARCHAR(255)|agent name|
|specialty| VARCHAR(225)| agents specialty|
|is_active|BOOLEAN|DEFAULT : TRUE|
|completed_missions|INT|DEFAULT : 0|
|failed_missions|INT| DEFAULT :0|
|agent_rank|ENUM|options are : Junior / Senior / Commander|

### Missions:
|column|type|info|
|----|----|----|
|id|INT, AUTO_INCREMENT, PRIMARY KEY|unique id|
|title|VARCHAR(50)|mission title|
|description|TEXT|mission description|
|location|VARCHAR(50)|mission location|
|difficulty|INT|1 - 10 only|
|importance|INT|1 - 10 only|
|status|VARCHAR(50)|DEFAULT : NEW|
|risk_level|VARCHAR(50)|automatically calculated, doesn't come from user|
|assigned_agent_id|INT|NULL till assignment|


## Database structure:
### DB_connection:

|method|job|
|----|----|
|get_connection()|connects to MYSQL|
|create_database()|will create the database if it doesn't exist|
|create_tables()|will create tables if they don't exist|

### AgentDB:

|method|job|
|----|----|
|create_agent()|creates new agent and returns id|
|get_all_agent()|returns list of all agents|
|get_agent_by_id(id)|returns specific agent by id or None|
|update_agent(id, data) | updates specified agent with new data (id cant be updated)|
|deactivate_agent(id)|deactivates specified agent|
|increment_completed(id)|updates number of completed missions for specified agent|
|increment_failed(id)|updates number of failed missions for specified agent|
|get_agent_performance(id)|returns dict with fields (completed, failed, total, success_rate) |
|count_active_agents()|returns number of active agents|

### MissionDB:

|method|job|
|----|----|
|create_mission()|creates new mission|
|get_all_missions()|returns all missions|
|get_mission_by_id(id)| returns specified mission or None|
|assign_mission(mission_id, agent_id)|assigns mission to agent|
|update_mission_status(id, status)| updates specified mission status|
|get_open_mission_by_agent(id)|returns missions where status is ASSIGNED/IN_PROGRESS|
|count_all_missions()|returns total missions|
|count_by_status(status)|counts missions by status|
|count_open_missions()|returns count of open missions|
|count_critical_missions()|returns count of missions where risk level is CRITICAL|
|get_top_agent()|returns agent with the most completed missions|


## System rules:

|rule no.|description|
|----|----|
|1|rank must be Junior / Senior / Commander anything else will result in error|
|2|'importance' and 'difficulty' must be between 1 - 10|
|3|risk_level is calculated automatically when created|
|4|agent with active=False cannot receive missions|
|5|agent cant have mor then 3 open missions (ASSIGNED / IN_PROGRESS)|
|6|if risk_level=CRITICAL only agent level Commandeer can take it|
|7|can only assign missions with status=NEW after assignment status=ASSIGNED|
|8|can only start a mission with status=ASSIGNED after start status=IN_PROGRESS|
|9|can only finnish mission with status=IN_PROGRESS and change status to failed or completed|
|10|can only abort mission if status is NEW or ASSIGNED else will result in a error|

## Run instructions:

#### run 
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
#### 
create a venv and activate it
####
install requirements.txt
####
create an instance of DB_connections and one of AgentDb and of MissionDB, 
or crate a main,  
run create_database() to insure it exists and run create_tables(),
can now preform the methods on the other classes



