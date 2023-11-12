from datetime import datetime

from alembic import op
import sqlalchemy as sa


revision = '667ju4rt550op'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.Text, nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime, default=datetime.now().replace(microsecond=0)))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about_me')
        batch_op.drop_column('last_seen')
