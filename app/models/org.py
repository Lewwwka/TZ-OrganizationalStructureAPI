import datetime
from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, func, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="NO ACTION"), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent: Mapped["Department | None"] = relationship(
        "Department", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Department"]] = relationship(
        "Department", back_populates="parent", cascade="all, delete-orphan"
    )
    employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="department", passive_deletes=True
    )

    __table_args__ = (Index("ix_unique_name_parent", "name", "parent_id", unique=True),)


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="NO ACTION"), nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    department: Mapped["Department"] = relationship(
        "Department", back_populates="employees"
    )
