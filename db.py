import aiosqlite
import sqlite3
import os

class DB():
    creates = """
        CREATE TABLE message_counter (user_id INT, last_user_name STRING, message_count INT)
    """
    def __init__(self, path):
        if not os.path.exists(path):
            with sqlite3.connect(path) as db:
                db.execute(DB.creates)
                db.commit()
        self.path = path
        self.cnt = 0

    async def add_count(self, user_id, mention):
        print(mention)
        if self.cnt==5:
            async with aiosqlite.connect(self.path) as db:
                await db.execute(
                    f"""
                        CREATE TABLE message_counter_tmp AS
                        SELECT message_counter.user_id, last_.last_user_name, SUM(message_count) as message_count
                        FROM message_counter
						JOIN (SELECT user_id, last_user_name FROM(
                            SELECT user_id, last_user_name, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY ROWID DESC) as rn 
                            FROM message_counter)
							where rn=1) as last_
						ON last_.user_id = message_counter.user_id
                        GROUP BY message_counter.user_id
                    """
                )
                await db.execute("DROP TABLE message_counter")
                await db.execute("ALTER TABLE message_counter_tmp RENAME TO message_counter;")
                await db.commit()
            self.cnt = 0
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                f"""
                    INSERT INTO message_counter (user_id, last_user_name, message_count)
                    VALUES ({user_id}, '{mention}', 1)
                """
            )
            await db.commit()
        self.cnt+=1
    
