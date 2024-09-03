"""Make SignOutTime in Attendance nullable

Revision ID: cacbd959e2ee
Revises: bd6290023305
Create Date: 2024-09-01 21:08:55.303541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cacbd959e2ee'
down_revision = 'bd6290023305'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.alter_column('signOutTime',
               existing_type=sa.TIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.alter_column('signOutTime',
               existing_type=sa.TIME(),
               nullable=False)

    # ### end Alembic commands ###
