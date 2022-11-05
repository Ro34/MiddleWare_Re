import sqlite3


class DatabaseBase:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = self.init_database()

    def init_database(self):
        conn = sqlite3.connect('mission.db')
        # c = conn.cursor()
        # c.execute(
        #     "create table if not exists ?(ID INTEGER PRIMARY KEY,TASKID INT,MISSIONTYPE STR,PLATFORMCONTEXT STR,SERVERCONTEXT STR,PID STR,PROGRESS INT)",
        #     (self.sql_name,))
        # c.execute(
        #     "create table if not exists marking_list(ID INTEGER PRIMARY KEY,TASKID INT,MISSIONTYPE STR,PLATFORMCONTEXT STR,SERVERCONTEXT STR,CONTAINERNAME STR)")
        # c.close()
        return conn

    # def insert_database(self, para):
    # conn = sqlite3.connect('mission.db')
    # c = conn.cursor()

    # c.execute(
    #     "insert into ?(ID,TASKID,MISSIONTYPE,PLATFORMCONTEXT,SERVERCONTEXT,CONTAINERNAME) values (NULL,?,?,?,?,?)",
    #     (self.sql_name,taskid, missionType, platformContext, taskid, conname))
    # c.close()
    # conn.commit()

    def update_database(self, update_key, update_value, update_condition_key, update_condition_value):
        # super().__init__('ServicesResourcesTable')
        # c = super().init_database()
        conn = sqlite3.connect('mission.db')
        c = conn.cursor()
        c.execute(
            # "UPDATE" + self.table_name + " SET " += ? WHERE ? = ? VALUES()"
            #https://lilongsy.blog.csdn.net/article/details/122883570?spm=1001.2101.3001.6650.3&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-3-122883570-blog-108942995.pc_relevant_3mothn_strategy_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-3-122883570-blog-108942995.pc_relevant_3mothn_strategy_recovery&utm_relevant_index=4
            "UPDATE " + self.table_name + " SET " + update_key + " =? "  + " WHERE " + update_condition_key + " =?",(update_value,update_condition_value))
        c.close()
        conn.commit()

    def query_database(self, query_condition_key, query_condition_value):
        # c = super().init_database()
        conn = sqlite3.connect('mission.db')

        def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d  

        c = conn.cursor()
        c.execute(
            "SELECT * FROM "+self.table_name+" WHERE "+query_condition_key +" = ?", (query_condition_value)
        )
        # print(c.fetchall())
        result_dict = dict_factory(c,c.fetchone())
        c.close()
        print(result_dict)
        self.dict = result_dict
        # return result_dict



class ServicesResources(DatabaseBase):
    def __init__(self):
        super().__init__('ServicesResourcesTable')
        # c = super().init_database()
        conn = self.conn
        c = conn.cursor()
        print(c)
        c.execute(
            "create table if not exists " + self.table_name + " (ID INTEGER PRIMARY KEY, SERVICE_NAME VARCHAR(100),GPU_ESTIMATE VARCHAR(100),CPU_ESTIMATE VARCHAR(100))")
        print(111)
        conn.commit()
        c.close()

    def insert_database(self, service_name, gpu_estimate, cpu_estimate):
        super().__init__('ServicesResourcesTable')
        conn = self.conn
        c = conn.cursor()
        c.execute(
            "insert into " + self.table_name + " (ID,SERVICE_NAME,GPU_ESTIMATE,CPU_ESTIMATE) values (NULL,'?','?','?')",
            (service_name, gpu_estimate, cpu_estimate)
        )

        c.close()
        conn.commit()

    def update_database(self, update_key, update_value, update_condition_key, update_condition_value):
        super().__init__('ServicesResourcesTable')
        # c = super().init_database()

        super().update_database(update_key, update_value, update_condition_key, update_condition_value)
        # c.execute(
        #     "UPDATE ? SET ? =? WHERE ?=?",
        #     (self.table_name, update_key, update_value, update_condition_key, update_condition_value)
        # )
        # c.close()

    def query_database(self, query_condition_key, query_condition_value):
        super().__init__('ServicesResourcesTable')
        super().query_database(query_condition_key, query_condition_value)


class ServerInfo(DatabaseBase):
    def __init__(self):
        super().__init__('ServerInfo')
        conn = self.conn
        c = conn.cursor()
        c.execute(
            "create table if not exists ? (ID INTEGER PRIMARY KEY, IP VARCHAR(50),STATUS VARCHAR(50),TYPE VARCHAR(50),MISSION_NUM VARCHAR(50),RESOURCES VARCHAR(50),NETWORK VARCHAR(50))",
            (self.table_name,))
        c.close()

    def insert_database(self, ip, status, type0, mission_num, resources, network):
        super().__init__('ServicesResourcesTable')
        c = super().init_database()
        c.execute(
            "insert into ?(ID,IP,STATUS,TYPE,MISSION_NUM,RESOURCES,NETWORK) values (NULL,?,?,?,?,?,?)",
            (self.table_name, ip, status, type0, mission_num, resources, network)
        )
        c.close()

    def update_database(self, update_key, update_value, update_condition_key, update_condition_value):
        super().__init__('ServicesResourcesTable')
        super().update_database(update_key, update_value, update_condition_key, update_condition_value)

    def query_database(self, column_name, query_condition_key, query_condition_value):
        super().__init__('ServicesResourcesTable')
        super().query_database(column_name, query_condition_key, query_condition_value)


class MissionInfo(DatabaseBase):
    def init_database(self):
        super().__init__('ServicesResourcesTable')
        c = super().init_database()
        c.execute(
            "create table if not exists ?(ID INTEGER PRIMARY KEY, TASKID INT,MISSIONTYPE VARCHAR(50),MISSIONSTATUS VARCHAR(50),IP VARCHAR(50),PORT VARCHAR(50),SERVERSTATUS VARCHAR(50),PLATFORMCONTEXT VARCHAR(255),SERVERCONTEXT VARCHAR(50),PID INT,PROGRESS FLOAT,CONTAINERNAME VARCHAR(50))",
            self.table_name)
        c.close()

    def insert_database(self, id, taskid, mission_type, missions_status, ip, port, server_status, platform_context,
                        server_context, pid, progress, containername):
        super().__init__('ServicesResourcesTable')
        c = super().init_database()
        c.execute(
            "insert into ?(ID,TASKID,MISSIONTYPE,MISSIONSTATUS,IP,PORT,SERVERSTATUS,PLATFORMCONTEXT,SERVERCONTEXT,PID,PROGRESS,CONTAINERNAME) values (NULL,?,?,?,?,?,?,?,?,?,?,?)",
            (self.table_name, id, taskid, mission_type, missions_status, ip, port, server_status, platform_context,
             server_context, pid, progress, containername)
        )
        c.close()

    def update_database(self, update_key, update_value, update_condition_key, update_condition_value):
        super().__init__('ServicesResourcesTable')
        super().update_database(update_key, update_value, update_condition_key, update_condition_value)

    def query_database(self, column_name, query_condition_key, query_condition_value):
        super().__init__('ServicesResourcesTable')
        super().query_database(column_name, query_condition_key, query_condition_value)


b = ServicesResources()

b.query_database('ID', '2')
print(b.dict)
# print(c)
