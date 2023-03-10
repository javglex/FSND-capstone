"""add user foreign key to listing model

Revision ID: 45fc1d9d19de
Revises: 
Create Date: 2023-01-29 10:29:41.174119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45fc1d9d19de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('People')
    op.add_column('Listing', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Listing', 'User', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Listing', type_='foreignkey')
    op.drop_column('Listing', 'user_id')
    op.create_table('People',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"People_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('catchphrase', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='People_pkey')
    )
    # ### end Alembic commands ###
