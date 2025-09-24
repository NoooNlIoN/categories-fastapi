from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.database.table import Base



class Client(Base):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)