"""create post table

Revision ID: 9f05292d7922
Revises: 
Create Date: 2023-02-16 20:21:07.487962

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '9f05292d7922'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
    sa.Column("title", sa.String, nullable=False),
    sa.Column("content", sa.String, nullable=False),
    sa.Column("is_published", sa.Boolean, nullable=False, server_default="false"),
    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now())
    )

def downgrade() -> None:
    op.drop_table("posts")