from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, LargeBinary, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    telegram_username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    
    poll_answers = relationship("PollAnswer", back_populates="user")
    embeddings = relationship("UserEmbedding", back_populates="user")

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    questions = Column(JSON)  # List[str]
    created_by_admin_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    answers = relationship("PollAnswer", back_populates="poll")

class PollAnswer(Base):
    __tablename__ = "poll_answers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    poll_id = Column(Integer, ForeignKey("polls.id"))
    answers = Column(JSON)  # Dict[idx, text]
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="poll_answers")
    poll = relationship("Poll", back_populates="answers")
    
    __table_args__ = (UniqueConstraint('user_id', 'poll_id'),)

class UserEmbedding(Base):
    __tablename__ = "user_embeddings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cluster_id = Column(Integer)
    embedding = Column(LargeBinary)
    user = relationship("User", back_populates="embeddings")