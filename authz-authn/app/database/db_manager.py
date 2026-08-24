from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# We wont use a config file so we define constants
POOL_SIZE = 4


class DatabaseManager:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, pool_size=POOL_SIZE)
        self._session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    @contextmanager
    def session(self) -> Iterator[Session]:
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self, base: type[DeclarativeBase]) -> None:
        base.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        return self._session_factory()
