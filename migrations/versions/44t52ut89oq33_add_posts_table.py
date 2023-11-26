from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.dialects import postgresql
from app.posts.models import EnumTopic

revision = '44t52ut89oq33'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('text', sa.Text, nullable=True),
        sa.Column('image_file', sa.String(length=200), nullable=False, server_default='postdefault.jpg'),
        sa.Column('created', sa.TIMESTAMP(), nullable=False, default=datetime.now().replace(microsecond=0)),
        sa.Column('type', sa.Enum(EnumTopic, name='enumtopictype'), nullable=False, default=EnumTopic.News),
        sa.Column('enabled', sa.Boolean(), nullable=True, default=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('posts')