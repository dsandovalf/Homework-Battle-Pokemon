"""empty message

Revision ID: d3aabd55b8a9
Revises: ac46dda3acd9
Create Date: 2021-11-03 09:51:07.748853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3aabd55b8a9'
down_revision = 'ac46dda3acd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.add_column('pokemon', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('pokemon', sa.Column('date_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pokemon', 'date_updated')
    op.drop_column('pokemon', 'date_created')
    op.drop_table('followers')
    # ### end Alembic commands ###