"""empty message

Revision ID: 37de7126ebb2
Revises: 77276bd0a416
Create Date: 2022-02-09 13:04:37.089638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37de7126ebb2'
down_revision = '77276bd0a416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pending_players_trips', sa.Column('trip_owner_username', sa.String(), nullable=True))
    op.drop_column('pending_players_trips', 'trip_owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pending_players_trips', sa.Column('trip_owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('pending_players_trips', 'trip_owner_username')
    # ### end Alembic commands ###