import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH", "./todo.db")

async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL
        )
        """)
        await db.commit()

async def add_task(title: str, description: str, completed: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO tasks (title, description, completed)
            VALUES (?, ?, ?)
        """, (title, description, completed))
        await db.commit()

async def get_tasks():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        result = await db.execute("""
        SELECT id, title, description, completed FROM tasks
        """)
        rows = await result.fetchall()
        return [dict(row) for row in rows]

async def get_task(task_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        result = await db.execute("""
        SELECT id, title, description, completed FROM tasks WHERE id = ?
        """, (task_id,))
        row = await result.fetchone()
        return dict(row) if row else None

async def update_task(task_id: int, title: str = None, description: str = None, completed: bool = None):
    update_count = 0
    if title is not None:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            result = await db.execute("""
                UPDATE tasks
                SET title = ?
                WHERE id = ?
                RETURNING id, title, description, completed
            """, (title, task_id))
            row = await result.fetchone()
            await db.commit()
            update_count += 1 if row else 0
    if description is not None:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            result = await db.execute("""
                UPDATE tasks
                SET description = ?
                WHERE id = ?
                RETURNING id, title, description, completed
            """, (description, task_id))
            row = await result.fetchone()
            await db.commit()
            update_count += 1 if row else 0
    if completed is not None:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            result = await db.execute("""
                UPDATE tasks
                SET completed = ?
                WHERE id = ?
                RETURNING id, title, description, completed
            """, (completed, task_id))
            row = await result.fetchone()
            await db.commit()
            update_count += 1 if row else 0
    return update_count

async def delete_task(task_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        result = await db.execute("""
        DELETE FROM tasks
        WHERE id = ?
        RETURNING id, title, description, completed
        """, (task_id,))
        row = await result.fetchone()
        await db.commit()
        return dict(row) if row else None