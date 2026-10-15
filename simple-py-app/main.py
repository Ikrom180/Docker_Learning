import os
from contextlib import asynccontextmanager
from pathlib import Path

import pg8000.dbapi
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent

# Defaults match your Docker Postgres on port 5433.
# Later, when the app also runs in Docker, set DB_HOST=postgresdb and DB_PORT=5432.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "user-account"),
}


def get_connection():
    return pg8000.dbapi.connect(**DB_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Postgres has tables (Mongo has collections), so create the table first.
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid    INTEGER PRIMARY KEY,
                name      TEXT,
                email     TEXT,
                interests TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    yield


app = FastAPI(lifespan=lifespan)

# Serves the profile picture from an "images" folder, if you have one.
if (BASE_DIR / "images").exists():
    app.mount("/images", StaticFiles(directory=BASE_DIR / "images"), name="images")


class Profile(BaseModel):
    name: str
    email: str
    interests: str


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/get-profile")
def get_profile():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT userid, name, email, interests FROM users WHERE userid = %s",
            (1,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return {}
    return {"userid": row[0], "name": row[1], "email": row[2], "interests": row[3]}


@app.post("/update-profile")
def update_profile(profile: Profile):
    print("connecting to the db...")
    conn = get_connection()
    print("successfully connected to the db")

    # Same idea as updateOne(..., {upsert: true}):
    # insert if the user does not exist, update if it does.
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (userid, name, email, interests)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (userid) DO UPDATE
            SET name = EXCLUDED.name,
                email = EXCLUDED.email,
                interests = EXCLUDED.interests
            """,
            (1, profile.name, profile.email, profile.interests),
        )
        conn.commit()
    finally:
        conn.close()
    print("successfully updated or inserted")

    return {"userid": 1, **profile.model_dump()}