from alembic import op
import sqlalchemy as sa


revision = '554noiw498iuy'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('image_file', type_=sa.String(length=200), unique=True, nullable=False)

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password', type_=sa.String(length=20), unique=True, nullable=False)
