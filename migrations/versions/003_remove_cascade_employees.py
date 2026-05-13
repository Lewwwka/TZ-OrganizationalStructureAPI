from typing import Sequence, Union
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("employees_department_id_fkey", "employees", type_="foreignkey")
    op.create_foreign_key(
        "employees_department_id_fkey",
        "employees",
        "departments",
        ["department_id"],
        ["id"],
        ondelete="NO ACTION",
    )


def downgrade() -> None:
    op.drop_constraint("employees_department_id_fkey", "employees", type_="foreignkey")
    op.create_foreign_key(
        "employees_department_id_fkey",
        "employees",
        "departments",
        ["department_id"],
        ["id"],
        ondelete="CASCADE",
    )
