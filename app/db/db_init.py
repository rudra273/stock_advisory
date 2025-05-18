from app.db.config import engine, Base
from app.models import stock  

def init_db():
    Base.metadata.create_all(bind=engine)
