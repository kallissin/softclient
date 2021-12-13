"""merging two heads

Revision ID: 7dc0ac050a72
Revises: 44283c41213d, 245c117c5f47
Create Date: 2021-12-13 12:15:36.961038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dc0ac050a72'
down_revision = ('44283c41213d', '245c117c5f47')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
