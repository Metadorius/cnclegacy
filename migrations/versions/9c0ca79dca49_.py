"""empty message

Revision ID: 9c0ca79dca49
Revises: 97ac4a4cc865
Create Date: 2019-05-09 16:09:16.521569

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9c0ca79dca49'
down_revision = '97ac4a4cc865'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file', 'file_loc',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=False)
    op.drop_index('file_url', table_name='file')
    op.drop_column('file', 'file_url')
    op.alter_column('menu_item', 'item_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=False)
    op.alter_column('menu_link', 'item_link',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=False)
    op.alter_column('menu_page', 'page_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('page', 'page_title',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64),
               nullable=False)
    op.alter_column('page', 'page_url',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64),
               nullable=False)
    op.alter_column('page', 'page_visible',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.alter_column('perm', 'perm_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=False)
    op.alter_column('role', 'role_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=False)
    op.alter_column('tag', 'tag_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=False)
    op.alter_column('user', 'role_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user', 'user_login',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_login',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=True)
    op.alter_column('user', 'role_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tag', 'tag_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=True)
    op.alter_column('role', 'role_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=True)
    op.alter_column('perm', 'perm_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=True)
    op.alter_column('page', 'page_visible',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('page', 'page_url',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64),
               nullable=True)
    op.alter_column('page', 'page_title',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64),
               nullable=True)
    op.alter_column('menu_page', 'page_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('menu_link', 'item_link',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=True)
    op.alter_column('menu_item', 'item_name',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32),
               nullable=True)
    op.add_column('file', sa.Column('file_url', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64), nullable=True))
    op.create_index('file_url', 'file', ['file_url'], unique=True)
    op.alter_column('file', 'file_loc',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               nullable=True)
    # ### end Alembic commands ###
