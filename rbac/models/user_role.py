import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    