import asyncpg
import asyncio
from contextlib import asynccontextmanager

HOST = '127.0.0.1'
USER = 'postgres'
PWD = 'postgres'
DB = 'tutorial_fastapi'



class DatabaseAsync:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn_str =  f'{self.user}://{self.password}@{self.host}/{self.database}'
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
            raise error
        finally:
            await conn.close()
            
    async def execute(self, query: str, params: tuple = None):
        async with self.connect() as conn:
            if params is None:
                await conn.execute(query)
            else:
                await conn.execute(query, *params)

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
    
    
if __name__ == '__main__':
    async def main():
        db = DatabaseAsync(host=HOST, user=USER, password=PWD, database=DB)
        print(db)
        # Executing a query
        await db.execute(
            "INSERT INTO test_database (content1, content2) VALUES ($1, $2)", 
            ('value1', 'value2'))

        # Fetching a single row
        row = await db.fetchone("SELECT * FROM test_database WHERE id = $1", (1,))
        print(row)

        # Fetching multiple rows
        rows = await db.fetchall("SELECT * FROM test_database")
        for row in rows:
            print(row)

    # Run the async main function
    asyncio.run(main())