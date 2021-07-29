"""empty message

Revision ID: 8fe520f16539
Revises: 
Create Date: 2021-07-23 19:52:39.578383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe520f16539'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_caps_data'), 'caps', ['data'], unique=False)
    op.create_table('implant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_implant_data'), 'implant', ['data'], unique=False)
    op.create_table('restorativeParts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restorativeParts_data'), 'restorativeParts', ['data'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('Report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('number', sa.String(length=32), nullable=True),
    sa.Column('doctor', sa.String(length=128), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('uncoverdate', sa.Date(), nullable=True),
    sa.Column('restoredate', sa.Date(), nullable=True),
    sa.Column('implant_id', sa.Integer(), nullable=True),
    sa.Column('cap_id', sa.Integer(), nullable=True),
    sa.Column('part_id', sa.Integer(), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('restore', sa.Text(), nullable=True),
    sa.Column('anesthetic', sa.Text(), nullable=True),
    sa.Column('tolerance', sa.String(length=32), nullable=True),
    sa.Column('rx', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cap_id'], ['caps.id'], ),
    sa.ForeignKeyConstraint(['implant_id'], ['implant.id'], ),
    sa.ForeignKeyConstraint(['part_id'], ['restorativeParts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Report')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_restorativeParts_data'), table_name='restorativeParts')
    op.drop_table('restorativeParts')
    op.drop_index(op.f('ix_implant_data'), table_name='implant')
    op.drop_table('implant')
    op.drop_index(op.f('ix_caps_data'), table_name='caps')
    op.drop_table('caps')
    # ### end Alembic commands ###
