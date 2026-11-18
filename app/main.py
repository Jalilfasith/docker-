import os

import redis
from flask import Flask, redirect, request
from markupsafe import escape

app = Flask(__name__)

database = redis.Redis(
    host=os.getenv("REDIS_HOST", "database"),
    port=6379,
    decode_responses=True,
)

@app.get("/")
def home():
    notes = database.lrange("notes", 0, -1)
    note_list = "".join(f"<li>{escape(note)}</li>" for note in notes)

    return f"""
    <h1>My Notes</h1>
    <form method="post" action="/add">
      <input name="note" placeholder="Write a note" required>
      <button>Save</button>
    </form>
    <ul>{note_list}</ul>
    """

@app.post("/add")
def add_note():
    note = request.form.get("note", "").strip()

    if note:
        database.lpush("notes", note)

    return redirect("/")

@app.get("/health")
def health():
    database.ping()
    return "healthy"