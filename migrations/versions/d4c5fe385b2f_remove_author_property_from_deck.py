"""Remove author property from deck

Revision ID: d4c5fe385b2f
Revises: b67147fc56c3
Create Date: 2023-10-29 13:45:04.115524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4c5fe385b2f'
down_revision = 'b67147fc56c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deck', schema=None) as batch_op:
        batch_op.drop_constraint('fk_deck_author_id', type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('deck', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('author_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(
            'fk_deck_author_id', 'user', ['author_id'], ['id'])

    # ### end Alembic commands ###
