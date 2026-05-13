from typing import Sequence, Union
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("departments_parent_id_fkey", "departments", type_="foreignkey")
    op.create_foreign_key(
        "departments_parent_id_fkey",
        "departments",
        "departments",
        ["parent_id"],
        ["id"],
        ondelete="NO ACTION",
    )


def downgrade() -> None:
    op.drop_constraint("departments_parent_id_fkey", "departments", type_="foreignkey")
    op.create_foreign_key(
        "departments_parent_id_fkey",
        "departments",
        "departments",
        ["parent_id"],
        ["id"],
        ondelete="CASCADE",
    )
