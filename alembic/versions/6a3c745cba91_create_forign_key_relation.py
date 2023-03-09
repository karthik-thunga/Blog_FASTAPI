"""create forign key relation

Revision ID: 6a3c745cba91
Revises: 45e9d53c8fa1
Create Date: 2023-02-16 20:52:41.626748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3c745cba91'
down_revision = '45e9d53c8fa1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
    sa.Column("owner_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key("posts_users_fk", 
    source_table="posts", 
    referent_table="users", 
    ondelete="CASCADE",
    local_cols=["owner_id"],
    remote_cols=["id"],
    )


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
