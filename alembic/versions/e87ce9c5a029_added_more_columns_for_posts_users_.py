"""added more columns for posts, users, comments

Revision ID: e87ce9c5a029
Revises: 90bf53bcc3cb
Create Date: 2023-02-19 19:31:51.199613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e87ce9c5a029'
down_revision = '90bf53bcc3cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('posts', sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    op.drop_column('posts', 'last_updated')
    op.drop_column('comments', 'created_at')
    # ### end Alembic commands ###
