from alembic import op
import sqlalchemy as sa

revision = '7196xfc21nil1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('feedback', sa.String(length=200), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('feedback')
