    from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
    from sqlalchemy.orm import declarative_base, relationship
    from sqlalchemy.sql import func
    from uuid import uuid4

    Base = declarative_base()

    class User(Base):
        __tablename__ = "users"

        id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
        username = Column(String, unique=True, index=True)
        hashed_password = Column(String)
        tasks = relationship("Task", back_populates="owner")
    class Task(Base):
      __tablename__ = "tasks"
      id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
      title = Column(String)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      completed = Column(Boolean, default=False)
      owner_id = Column(String, ForeignKey("users.id"))
      owner = relationship("User", back_populates="tasks")
