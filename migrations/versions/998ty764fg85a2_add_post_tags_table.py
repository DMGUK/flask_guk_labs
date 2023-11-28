from alembic import op
import sqlalchemy as sa

revision = '998ty764fg85a2'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'post_tags',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )

    op.create_foreign_key('fk_post_tags_post_id', 'post_tags', 'posts', ['post_id'], ['id'])
    op.create_foreign_key('fk_post_tags_tag_id', 'post_tags', 'tags', ['tag_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_post_tags_tag_id', 'post_tags', type_='foreignkey')
    op.drop_constraint('fk_post_tags_post_id', 'post_tags', type_='foreignkey')
    op.drop_table('post_tags')