from alembic import op
import sqlalchemy as sa

revision = '7132fgc6u7ipo9'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), unique=True, nullable=False),
        sa.Column('email', sa.String(length=200), unique=True, nullable=False),
        sa.Column('image_file', sa.String(20), nullable=False, server_default='default.jpg'),
        sa.Column('password', sa.String(60), unique=True, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('feedback')
