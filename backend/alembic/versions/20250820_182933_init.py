from alembic import op
import sqlalchemy as sa
revision = '20250820_182933'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('chat_logs', sa.Column('id', sa.Integer, primary_key=True), sa.Column('visitor_id', sa.String(64), nullable=False), sa.Column('role', sa.String(16), nullable=False), sa.Column('text', sa.Text, nullable=False), sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False))
    op.create_index('ix_chat_logs_visitor_id','chat_logs',['visitor_id'])
    op.create_table('feedback', sa.Column('id', sa.Integer, primary_key=True), sa.Column('comment', sa.Text, nullable=False), sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False))

def downgrade():
    op.drop_table('feedback')
    op.drop_index('ix_chat_logs_visitor_id', table_name='chat_logs')
    op.drop_table('chat_logs')
