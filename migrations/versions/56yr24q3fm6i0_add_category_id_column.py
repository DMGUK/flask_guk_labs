from alembic import op
import sqlalchemy as sa

revision = '56yr24q3fm6i0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_posts_category_id', 'posts', 'categories', ['category_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_posts_category_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'category_id')