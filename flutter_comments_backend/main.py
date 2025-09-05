#Packagesfrom 
fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# 1. Setting up the database
# -----------------------------
# SQLite database file named "comments.db" in the same folder.
# To store the data's in our computer.
SQLALCHEMY_DATABASE_URL = "sqlite:///./comments.db"

# Connecting with database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
 
# -----------------------------
# 2. Define the database table
# -----------------------------
class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each comment
    text = Column(String, index=True)  # The actual comment text

Base.metadata.create_all(bind=engine)

# -----------------------------
# 3. Setting up FastAPI app
# -----------------------------
app = FastAPI()  

# Frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  # HTTP requests (GET, POST)
    allow_headers=["*"],  
)


class Comment(BaseModel):
    text: str

# -----------------------------
# 5. To get all the comments
# -----------------------------
@app.get("/comments")
def get_comments():
    db = SessionLocal()  
    comments = db.query(CommentDB).all()  
    db.close()  
    # Return comments as a list of dictionaries 
    # for the user to view the existing comments
    return [{"id": c.id, "text": c.text} for c in comments]

# -----------------------------
# 6. Add a new comment
# -----------------------------
@app.post("/comments")
def add_comment(comment: Comment):
    db = SessionLocal()  
    new_comment = CommentDB(text=comment.text)  
    db.add(new_comment)  
    db.commit()  
    db.refresh(new_comment)  
    db.close()  
    return {"message": "Comment added successfully"}   
 