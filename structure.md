
## module  middleware_management
### class heartbeat
#### function
1. heartbeat()

## module  mission_management

### def mission_parse()

### class mission_start
#### interface
1. 
2. 
#### function

1. resources_query()
2. mission_distribute()
3. mission_start_AI_training()
4. mission_start_AI_marking()
5. creating_mission_item()

### class mission_maintain
#### function
1. parse_heartbeat()
2. update_progress()
3. update_database()

### class mission_stop
#### interface
1. post

#### function
1. get_mission_info()
2. mission_stop_AI_training(self):
3. mission_stop_AI_marking(self):


## module  database_management
#### interface
1. 
2. 
#### function
1. init_database()
2. insert_database()
3. update_database()
4. query_database()