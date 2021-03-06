"""change to posting

Revision ID: 4d90ca786ad7
Revises: 975eb19f8cec
Create Date: 2021-10-16 13:44:33.222179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d90ca786ad7'
down_revision = '975eb19f8cec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posting', 'img',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posting', 'img',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
