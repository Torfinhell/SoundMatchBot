from backend.database import engine, Base
from backend.models import User, Poll, PollAnswer, UserEmbedding
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")