"""create user table

Revision ID: 45e9d53c8fa1
Revises: 9f05292d7922
Create Date: 2023-02-16 20:31:06.838154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45e9d53c8fa1'
down_revision = '9f05292d7922'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
    sa.Column("first_name", sa.String, nullable=True),
    sa.Column("last_name", sa.String, nullable=True),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
    sa.Column("is_superuser", sa.Boolean, nullable=False, server_default="false"),
    )

def downgrade() -> None:
    op.drop_table("users")
