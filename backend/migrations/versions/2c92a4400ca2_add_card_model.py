"""Add card model

Revision ID: 2c92a4400ca2
Revises: 05773b7b4977
Create Date: 2023-09-16 09:31:25.465336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c92a4400ca2'
down_revision = '05773b7b4977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('front', sa.String(length=100), nullable=False),
    sa.Column('back', sa.String(length=100), nullable=False),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.id'], name='fk_card_deck_id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    # ### end Alembic commands ###