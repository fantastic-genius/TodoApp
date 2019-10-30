"""empty message

Revision ID: 647138b3928f
Revises: c9d48d904377
Create Date: 2019-10-25 15:39:36.547038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '647138b3928f'
down_revision = 'c9d48d904377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###