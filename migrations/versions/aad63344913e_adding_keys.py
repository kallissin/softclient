"""adding keys

Revision ID: aad63344913e
Revises: 2fb048eeae99
Create Date: 2021-12-08 17:31:28.796907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aad63344913e'
down_revision = '2fb048eeae99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cnpj', sa.String(length=18), nullable=False),
    sa.Column('trading_name', sa.String(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('key_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['key_id'], ['keys.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_id'),
    sa.UniqueConstraint('trading_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('companies')
    op.drop_table('keys')
    # ### end Alembic commands ###
