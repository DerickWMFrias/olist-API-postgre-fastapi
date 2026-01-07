from sqlalchemy.orm import sessionmaker

def create_sessionmaker(engine):
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )