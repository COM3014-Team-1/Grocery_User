from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '4356c3143dac'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Enable the "uuid-ossp" extension if it's not already enabled
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    
    # Drop the dependent tables first (if they exist) because we're recreating them.
    op.drop_table('login_events')
    op.drop_table('signup_events')
    op.drop_table('user')

    # Re-create the "user" table with a UUID primary key
    op.create_table(
        'user',
        sa.Column('user_id', UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.Text, nullable=False),
        sa.Column('phone', sa.String(50)),
        sa.Column('address', sa.String(255)),
        sa.Column('city', sa.String(100)),
        sa.Column('state', sa.String(100)),
        sa.Column('zipcode', sa.String(20)),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Re-create the signup_events table with the new foreign key type (UUID)
    op.create_table(
        'signup_events',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Re-create the login_events table with the new foreign key type (UUID)
    op.create_table(
        'login_events',
        sa.Column('id', UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.user_id'), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('success', sa.Boolean, nullable=False)
    )

def downgrade():
    # In downgrade, drop the newly created tables
    op.drop_table('login_events')
    op.drop_table('signup_events')
    op.drop_table('user')


