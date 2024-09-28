import asyncpg
import asyncio
from contextlib import asynccontextmanager


class DatabaseAsync:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn_str =  f'{self.user}://{self.password}@{self.host}:{self.port}/{self.database}'
        return
    
    
    async def get_connection(self):
        return await asyncpg.connect(self.conn_str)
        
    
    @asynccontextmanager
    async def connect(self):
        conn = await self.get_connection()
        try:
            yield conn
        except Exception as e:
            error = f'<Error in Database> {str(e)}'
            raise e
        finally:
            await conn.close()
            
    async def execute(self, query: str, params: tuple = None):
        async with self.connect() as conn:
            if params is None:
                await conn.execute(query)
            else:
                await conn.execute(query, *params)
    
    async def execute_and_get_record(self, query: str, params: tuple = None):
        query = query + ' RETURNING *'
        async with self.connect() as conn:
            if params is None:
                row = await conn.fetchrow(query)
            else:
                row = await conn.fetchrow(query, *params)
        return dict(row) if row else None
                

    async def fetchone(self, query: str, params: tuple = None):
        async with self.connect() as conn:
            if params is None:
                row = await conn.fetchrow(query)
            else:
                row = await conn.fetchrow(query, *params)
        return dict(row) if row else None

    async def fetchall(self, query: str, params: tuple = None):
        async with self.connect() as conn:
            if params is None:
                rows = await conn.fetch(query)
            else:
                rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows] if rows else []

    def read_sql(self, file_name):
        with open(os.path.join('queries', f'{file_name}.sql'), 'r') as f:
            data = f.read()
        return data
    
