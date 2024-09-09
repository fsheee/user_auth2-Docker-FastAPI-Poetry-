from sqlmodel import create_engine, SQLModel, Session # type: ignore
from app import settings



connection_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")


engine = create_engine(connection_string, connect_args={},
                       pool_recycle=300)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# from sqlmodel import create_engine, SQLModel, Session # type: ignore
# from app import settings

# # Create the connection string
# connection_string: str = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg2")

# # Create the database engine
# engine = create_engine(connection_string, connect_args={}, pool_recycle=300)

# # Create tables based on SQLModel metadata
# def create_tables():
#     SQLModel.metadata.create_all(engine)

# # Create a session generator
# def get_session():
#     with Session(engine) as session:
#         yield session
