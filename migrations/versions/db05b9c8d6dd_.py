"""empty message

Revision ID: db05b9c8d6dd
Revises: 64ff686825d6
Create Date: 2021-11-03 14:21:38.247224

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'db05b9c8d6dd'
down_revision = '64ff686825d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('followers')
    op.drop_column('pokemon', 'date_updated')
    op.drop_column('pokemon', 'date_created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pokemon', sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('pokemon', sa.Column('date_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_table('followers',
    sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('followed_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], name='followers_followed_id_fkey'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='followers_follower_id_fkey')
    )
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='post_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey')
    )
    # ### end Alembic commands ###
