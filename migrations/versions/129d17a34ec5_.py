"""empty message

Revision ID: 129d17a34ec5
Revises: f942d4e2f589
Create Date: 2018-10-03 09:42:43.540922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129d17a34ec5'
down_revision = 'f942d4e2f589'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('title', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'title')
    # ### end Alembic commands ###
