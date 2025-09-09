from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Temporary in-memory store
comments = []

class Comment(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

# To Fetch all comments
@app.get("/comments", response_model=List[Comment])
def get_comments():
    return comments

# To Post a new comment
@app.post("/comments")
def add_comment(comment: Comment):
    comments.append(comment)
    return {"message": "Comment added successfully", "comment": comment}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allowing frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:8000", "http://localhost:1234"] for stricter rules
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory store 
comments = []

class Comment(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/comments", response_model=List[Comment])
def get_comments():
    return comments

@app.post("/comments")
def add_comment(comment: Comment):
    comments.append(comment)
    return {"message": "Comment added successfully", "comment": comment}
