"""empty message

Revision ID: 175a0d271b9d
Revises: 8fe520f16539
Create Date: 2021-07-26 18:23:54.596445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '175a0d271b9d'
down_revision = '8fe520f16539'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_caps_data', table_name='caps')
    op.create_index(op.f('ix_caps_data'), 'caps', ['data'], unique=True)
    op.drop_index('ix_implant_data', table_name='implant')
    op.create_index(op.f('ix_implant_data'), 'implant', ['data'], unique=True)
    op.drop_index('ix_restorativeParts_data', table_name='restorativeParts')
    op.create_index(op.f('ix_restorativeParts_data'), 'restorativeParts', ['data'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_restorativeParts_data'), table_name='restorativeParts')
    op.create_index('ix_restorativeParts_data', 'restorativeParts', ['data'], unique=False)
    op.drop_index(op.f('ix_implant_data'), table_name='implant')
    op.create_index('ix_implant_data', 'implant', ['data'], unique=False)
    op.drop_index(op.f('ix_caps_data'), table_name='caps')
    op.create_index('ix_caps_data', 'caps', ['data'], unique=False)
    # ### end Alembic commands ###
