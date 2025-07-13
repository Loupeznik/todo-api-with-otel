from sqlalchemy import Column
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Column[int]
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr  # type: ignore
    def __tablename__(cls):
        return cls.__name__.lower() + "s"
