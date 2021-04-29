import asyncio
import asyncpg as pg
import os
import ssl
ssl_object = ssl.create_default_context(capath='rds-ca-2015-root.pem')
ssl_object.check_hostname = False
ssl_object.verify_mode = ssl.CERT_NONE

HOST = os.environ['DB_HOST']
DATABASE = os.environ['DATABASE']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

loop = asyncio.get_event_loop()
POOL = loop.run_until_complete(pg.create_pool(host = HOST, database = DATABASE, user = USERNAME, password = PASSWORD, ssl = ssl_object))


async def get_members():
    global POOL
    async with POOL.acquire() as connection:
        async with connection.transaction():
            record = await connection.fetch(
                '''
                SELECT user_id FROM todo_remind;
                '''
            )
            members = [id for row in record for id in row.values()]
    return members


async def get_tasks(member_id):
    global POOL
    async with POOL.acquire() as connection:
        async with connection.transaction():
            record = await connection.fetch(
                '''
                SELECT task, datetime FROM todo_remind WHERE user_id = $1;
                ''', member_id
            )
            tasks_tuple = []
            for row in record:
                values = []
                for i in row.values():
                    values.append(i)
                tasks_tuple.append(tuple(values))
    
    return tuple(tasks_tuple)

async def get_min_datetime():
    global POOL
    async with POOL.acquire() as connection:
        async with connection.transaction():
            record = await connection.fetch(
                '''
                SELECT user_id, task, datetime FROM todo_remind;
                '''
            )
            tasks_tuple = []
            for row in record:
                values = []
                for i in row.values():
                    values.append(i)
                tasks_tuple.append(tuple(values))
            datetime = [x for x in tasks_tuple if x[2] is not None]
    return datetime

async def get_remaining_task(datetime):
    global POOL
    async with POOL.acquire() as connection:
        async with connection.transaction():
            record = await connection.fetch(
                '''
                SELECT task FROM todo_remind WHERE date;
                '''
            )
            datetime = [i for row in record for i in row.values()]
            datetime = [x for x in datetime if x is not None]
    return datetime

async def to_csv():
    global POOL
    async with POOL.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                '''
                \copy (SELECT * FROM todo_remind)
                TO 'todo_backup.csv'
                DELIMITER ',' CSV HEADER;
                '''
            )


class ToDo():

    def __init__(self, member_id):
        self.member_id = member_id
        self.members = None
        self.pool = POOL

    async def mems(self):
        self.members = await get_members()
        return self.members

    async def all_tasks(self):
        return await get_tasks(self.member_id)

    async def todo_add(self, task, time):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    INSERT INTO todo_remind (user_id, task, datetime)
                    VALUES ($1, $2, $3);
                    ''', self.member_id, task, time)
        
    async def todo_remove(self, index):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                tasks = await get_tasks(self.member_id)
                task, time = tasks[index-1]
                await connection.execute(
                    '''
                    DELETE FROM todo_remind WHERE user_id = $1 AND task = $2 AND datetime = $3;
                    ''', self.member_id, task, time
                )

    async def todo_remove_all(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    DELETE FROM todo_remind WHERE user_id = $1;
                    ''', self.member_id
                )
