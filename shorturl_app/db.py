import aiosqlite
from pydantic import HttpUrl

DB_PATH = '/app/data/shorturl.db'

async def create_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
        )
        """)
        await db.commit()

async def add_url(url: HttpUrl):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        result = await db.execute("""
            INSERT INTO urls (url)
            VALUES (?)
            RETURNING id, url
        """, (str(url),))
        row = await result.fetchone()
        await db.commit()
        return dict(row)

async def get_url(url_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        result = await db.execute("""
        SELECT id, url FROM urls WHERE id = ?
        """, (url_id,))
        row = await result.fetchone()
        return dict(row) if row else None

