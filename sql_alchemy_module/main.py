# import sqlalchemy

# print(sqlalchemy.__version__)

# import sqlalchemy

# from typing import List
# from typing import Optional
# from sqlalchemy import MetaData
# from sqlalchemy import Table, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy import String, ForeignKey
# from sqlalchemy import create_engine
# from sqlalchemy import text

# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# engine = create_engine("sqlite:///example.db", echo=True)


# print( sqlalchemy.__version__)


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT 'hello world'"))
#     print(result.all())

# with engine.connect() as conn:
#     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
#     )

#     conn.commit()


# with engine.begin() as conn:
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
#     )

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
#     for row in result:
#         print(f"x: {row.x} y: {row.y}")

# stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

# with Session(engine) as session:
#     result = session.execute(stmt, {"y": 6})
#     for row in result:
#         print(f"x: {row.x} y: {row.y}")

# metadata_obj = MetaData()

# user_table = Table(
#     "user_account",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(30)),
#     Column("fullname", String),
# )

# address_table = Table(
#     "address",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("user_id",ForeignKey("user_account.id"), nullable=False), #type: ignore
#     Column("email_address", String, nullable=False),
# )

# metadata_obj.create_all(engine)

# from sqlalchemy.orm import DeclarativeBase

# class Base(DeclarativeBase):
#     pass


# engine = create_engine("sqlite:///example.db", echo=True)


# class Base(DeclarativeBase):
#     pass


# class User(Base):
#     __tablename__ = "user_account"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     fullname: Mapped[Optional[str]]

#     addresses: Mapped[List["Address"]] = relationship(back_populates="user")

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id = mapped_column(ForeignKey("user_account.id"))

#     user: Mapped[User] = relationship(back_populates="addresses")

#     def __repr__(self) -> str:
#         return f"Addresses(id={self.id!r}, email_address={self.email_address!r})"


# some_table = Table("some_table", Base.metadata, autoload_with=engine)


# Base.metadata.create_all(engine)

# print(f"{some_table!r}")

# from sqlalchemy import insert
# stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")

# compiled = stmt.compile()

# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()
#     print(result.inserted_primary_key)

# from sqlalchemy import insert

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(user_table),
#         [
#             {"name": "sandy", "fullname": "Sandy Cheeks"},
#             {"name": "patrick", "fullname": "Patrick Star"},
#         ],
#     )
#     conn.commit()


# from sqlalchemy import insert
# from sqlalchemy import select, bindparam

# scalar_subq = (
#     select(user_table.c.id)
#     .where(user_table.c.name == bindparam("username"))
#     .scalar_subquery()
# )

# with engine.connect() as conn:
#     result = conn.execute(
#         insert(address_table).values(user_id=scalar_subq),
#         [
#             {
#                 "username": "spongebob",
#                 "email_address": "spongebob@sqlalchemy.org",
#             },
#             {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
#             {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
#         ],
#     )
#     conn.commit()

# print("DONE")
