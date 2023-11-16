from alembic import op
import sqlalchemy as sa

revision = '31bt56x7u409'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'todo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('complete', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('todo')
