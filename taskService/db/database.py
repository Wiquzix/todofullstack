    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from models import Base
    from dotenv import load_dotenv

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/db")

    engine = create_engine(DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    def get_db():
        db = SessionLocal()
        try:
           yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
