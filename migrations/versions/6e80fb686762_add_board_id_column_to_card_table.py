"""Add board_id column to Card table

Revision ID: 6e80fb686762
Revises: b708c9ff88af
Create Date: 2025-06-24 20:09:25.941746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e80fb686762'
down_revision = 'b708c9ff88af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('board_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'board', ['board_id'], ['board_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('board_id')

    # ### end Alembic commands ###
