"""Add last_revised column

Revision ID: 0929ac05522b
Revises: d4c5fe385b2f
Create Date: 2023-10-29 15:22:24.197879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0929ac05522b'
down_revision = 'd4c5fe385b2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('last_revised', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('last_revised')

    # ### end Alembic commands ###
