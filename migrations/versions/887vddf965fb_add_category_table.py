from alembic import op
import sqlalchemy as sa

revision = '887vddf965fb'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )

def downgrade():
    op.drop_table('categories')