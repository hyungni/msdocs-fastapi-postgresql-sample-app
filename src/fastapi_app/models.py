import os
import typing
from datetime import datetime
from urllib.parse import quote_plus
from sqlmodel import Field, SQLModel, create_engine

sql_url = ""
if os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING"):
    env_connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")

    # Parse the connection string
    details = dict(item.split('=') for item in env_connection_string.split())

    # Properly format the URL for SQLAlchemy
    sql_url = (
        f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
        f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
    )

else:
    POSTGRES_USERNAME = os.environ.get("DBUSER")
    POSTGRES_PASSWORD = os.environ.get("DBPASS")
    POSTGRES_HOST = os.environ.get("DBHOST")
    POSTGRES_DATABASE = os.environ.get("DBNAME")
    POSTGRES_PORT = os.environ.get("DBPORT", 5432)
    POSTGRES_SSL = os.environ.get("DBSSL")

    sql_url = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    if POSTGRES_SSL:
        sql_url = f"{sql_url}?sslmode={POSTGRES_SSL}"

engine = create_engine(sql_url)


def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)

class Restaurant(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    street_address: str = Field(max_length=50)
    description: str = Field(max_length=250)

    def __str__(self):
        return f"{self.name}"

class Review(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    restaurant: int = Field(foreign_key="restaurant.id")
    user_name: str = Field(max_length=50)
    rating: typing.Optional[int]
    review_text: str = Field(max_length=500)
    review_date: datetime

    def __str__(self):
        return f"{self.name}"
