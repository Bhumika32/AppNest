"""initial clean schema (PRODUCTION READY FINAL)"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'c222c540e41e'
down_revision: Union[str, None] = None
branch_labels = None
depends_on = None


def upgrade():

    # --------------------- ACHIEVEMENTS ---------------------
    op.create_table(
        'achievements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key', sa.String(100), nullable=False, unique=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text())
    )

    # --------------------- MODULES ---------------------
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('type', sa.Enum('game', 'tool', name='module_type', native_enum=False), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('icon', sa.String(50)),
        sa.Column('thumbnail', sa.String(255)),
        sa.Column('component_key', sa.String(100), nullable=False),
        sa.Column('category', sa.String(50)),
        sa.Column('difficulty', sa.String(50)),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('capabilities', sa.JSON()),
        sa.Column('xp_reward_base', sa.Integer(), nullable=False, server_default=sa.text('10')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )

    op.create_index('idx_module_type_active', 'modules', ['type', 'is_active'])
    op.create_index('ix_modules_slug', 'modules', ['slug'], unique=True)

    # --------------------- ROLES ---------------------
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'))
    )

    # --------------------- USERS ---------------------
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('avatar_url', sa.String(255)),
        sa.Column('bio', sa.String(500)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('deleted_at', sa.DateTime()),
        sa.Column('last_login_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
    )

    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_last_login_at', 'users', ['last_login_at'])

    # --------------------- FEEDBACK ---------------------
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_index('ix_feedback_user_id', 'feedback', ['user_id'])

    # --------------------- QUESTS ---------------------
    op.create_table(
        'quests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('module_id', sa.Integer()),
        sa.Column('target_value', sa.Integer()),
        sa.Column('xp_reward', sa.Integer(), nullable=False, server_default=sa.text('10')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
    )

    op.create_index('ix_quests_module_id', 'quests', ['module_id'])

    # --------------------- GAME SESSIONS ---------------------
    op.create_table(
        'game_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('duration_seconds', sa.Integer()),
        sa.Column('meta', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
    )

    op.create_index('idx_game_user_module', 'game_sessions', ['user_id', 'module_id'])
    op.create_index('ix_game_sessions_user_id', 'game_sessions', ['user_id'])
    op.create_index('ix_game_sessions_module_id', 'game_sessions', ['module_id'])

    # --------------------- LEADERBOARD ---------------------
    op.create_table(
        'leaderboards',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('top_score', sa.Integer(), nullable=False),
        sa.Column('last_updated', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
        sa.UniqueConstraint('user_id', 'module_id', name='uq_user_module_score'),
    )

    op.create_index('idx_leaderboard_module_score', 'leaderboards', ['module_id', 'top_score'])
    op.create_index('ix_leaderboards_user_id', 'leaderboards', ['user_id'])
    op.create_index('ix_leaderboards_module_id', 'leaderboards', ['module_id'])

    # --------------------- MODULE ANALYTICS ---------------------
    op.create_table(
        'module_analytics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('duration', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
    )

    op.create_index('idx_module_event', 'module_analytics', ['module_id', 'event_type'])
    op.create_index('ix_module_analytics_user_id', 'module_analytics', ['user_id'])
    op.create_index('ix_module_analytics_module_id', 'module_analytics', ['module_id'])

    # --------------------- NOTIFICATIONS ---------------------
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('read_at', sa.DateTime()),
        sa.Column('data', sa.JSON()),
        sa.Column('action_url', sa.String(255)),
        sa.Column('priority', sa.String(20)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('expires_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_index('idx_notification_user_read', 'notifications', ['user_id', 'is_read'])
    op.create_index('ix_notifications_user_id', 'notifications', ['user_id'])

    # --------------------- OTP TOKENS ---------------------
    op.create_table(
        'otp_tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('otp_hash', sa.String(255), nullable=False),
        sa.Column('purpose', sa.String(50), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_index('idx_otp_user_purpose', 'otp_tokens', ['user_id', 'purpose'])

    # --------------------- SESSIONS ---------------------
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('refresh_token_hash', sa.String(255), nullable=False, unique=True),
        sa.Column('device_info', sa.String(255)),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('last_used_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_index('idx_session_user_active', 'sessions', ['user_id', 'revoked'])
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'])

    # --------------------- USER ACHIEVEMENTS ---------------------
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id']),
        sa.UniqueConstraint('user_id', 'achievement_id'),
    )

    # --------------------- USER PROGRESSION ---------------------
    op.create_table(
        'user_progression',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total_xp', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('level', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('rank_title', sa.String(100)),
        sa.Column('streak_count', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('last_activity_date', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_index('ix_user_progression_user_id', 'user_progression', ['user_id'], unique=True)

    # --------------------- USER QUESTS ---------------------
    op.create_table(
        'user_quests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('quest_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20)),
        sa.Column('progress', sa.Integer()),
        sa.Column('completed_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['quest_id'], ['quests.id']),
        sa.UniqueConstraint('user_id', 'quest_id'),
    )

    op.create_index('idx_user_quest_status', 'user_quests', ['user_id', 'status'])

    # --------------------- XP TRANSACTIONS ---------------------
    op.create_table(
        'xp_transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer()),
        sa.Column('xp_awarded', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('reason', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id']),
    )

    op.create_index('idx_xp_user_time', 'xp_transactions', ['user_id', 'created_at'])


def downgrade():
    op.drop_table('xp_transactions')
    op.drop_table('user_quests')
    op.drop_table('user_progression')
    op.drop_table('user_achievements')
    op.drop_table('sessions')
    op.drop_table('otp_tokens')
    op.drop_table('notifications')
    op.drop_table('module_analytics')
    op.drop_table('leaderboards')
    op.drop_table('game_sessions')
    op.drop_table('quests')
    op.drop_table('feedback')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('modules')
    op.drop_table('achievements')

# """initial clean schema

# Revision ID: c222c540e41e
# Revises: 
# Create Date: 2026-03-19 12:00:19.706781

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa

# # revision identifiers, used by Alembic.
# revision: str = 'c222c540e41e'
# down_revision: Union[str, None] = None
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('achievements',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('key', sa.String(length=100), nullable=False),
#     sa.Column('title', sa.String(length=200), nullable=False),
#     sa.Column('description', sa.Text(), nullable=True),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('key')
#     )
#     op.create_table('modules',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('name', sa.String(length=100), nullable=False),
#     sa.Column('slug', sa.String(length=100), nullable=False),
#     sa.Column('type', sa.Enum('game', 'tool', name='module_type'), nullable=False),
#     sa.Column('description', sa.Text(), nullable=True),
#     sa.Column('icon', sa.String(length=50), nullable=True),
#     sa.Column('thumbnail', sa.String(length=255), nullable=True),
#     sa.Column('component_key', sa.String(length=100), nullable=False),
#     sa.Column('category', sa.String(length=50), nullable=True),
#     sa.Column('difficulty', sa.String(length=50), nullable=True),
#     sa.Column('is_active', sa.Boolean(), nullable=False),
#     sa.Column('capabilities', sa.JSON(), nullable=True),
#     sa.Column('xp_reward_base', sa.Integer(), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_module_type_active', 'modules', ['type', 'is_active'], unique=False)
#     op.create_index(op.f('ix_modules_slug'), 'modules', ['slug'], unique=True)
#     op.create_table('roles',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('name', sa.String(length=50), nullable=False),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('name')
#     )
#     op.create_table('quests',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('title', sa.String(length=100), nullable=False),
#     sa.Column('description', sa.Text(), nullable=True),
#     sa.Column('module_id', sa.Integer(), nullable=True),
#     sa.Column('target_value', sa.Integer(), nullable=True),
#     sa.Column('xp_reward', sa.Integer(), nullable=True),
#     sa.Column('is_active', sa.Boolean(), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_quests_module_id'), 'quests', ['module_id'], unique=False)
#     op.create_table('users',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('username', sa.String(length=50), nullable=False),
#     sa.Column('email', sa.String(length=120), nullable=False),
#     sa.Column('role_id', sa.Integer(), nullable=False),
#     sa.Column('password_hash', sa.String(length=255), nullable=False),
#     sa.Column('is_verified', sa.Boolean(), nullable=False),
#     sa.Column('is_active', sa.Boolean(), nullable=False),
#     sa.Column('avatar_url', sa.String(length=255), nullable=True),
#     sa.Column('bio', sa.String(length=500), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.Column('deleted_at', sa.DateTime(), nullable=True),
#     sa.Column('last_login_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
#     op.create_index(op.f('ix_users_last_login_at'), 'users', ['last_login_at'], unique=False)
#     op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
#     op.create_table('feedback',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('rating', sa.Integer(), nullable=False),
#     sa.Column('message', sa.Text(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_feedback_user_id'), 'feedback', ['user_id'], unique=False)
#     op.create_table('game_sessions',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('module_id', sa.Integer(), nullable=False),
#     sa.Column('score', sa.Integer(), nullable=False),
#     sa.Column('duration_seconds', sa.Integer(), nullable=True),
#     sa.Column('metadata', sa.JSON(), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_game_user_module', 'game_sessions', ['user_id', 'module_id'], unique=False)
#     op.create_index(op.f('ix_game_sessions_module_id'), 'game_sessions', ['module_id'], unique=False)
#     op.create_index(op.f('ix_game_sessions_user_id'), 'game_sessions', ['user_id'], unique=False)
#     op.create_table('leaderboards',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('module_id', sa.Integer(), nullable=False),
#     sa.Column('top_score', sa.Integer(), nullable=False),
#     sa.Column('last_updated', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('user_id', 'module_id', name='uq_user_module_score')
#     )
#     op.create_index('idx_leaderboard_module_score', 'leaderboards', ['module_id', 'top_score'], unique=False)
#     op.create_index(op.f('ix_leaderboards_module_id'), 'leaderboards', ['module_id'], unique=False)
#     op.create_index(op.f('ix_leaderboards_user_id'), 'leaderboards', ['user_id'], unique=False)
#     op.create_table('module_analytics',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('module_id', sa.Integer(), nullable=False),
#     sa.Column('event_type', sa.String(length=50), nullable=False),
#     sa.Column('duration', sa.Integer(), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_module_event', 'module_analytics', ['module_id', 'event_type'], unique=False)
#     op.create_index(op.f('ix_module_analytics_created_at'), 'module_analytics', ['created_at'], unique=False)
#     op.create_index(op.f('ix_module_analytics_event_type'), 'module_analytics', ['event_type'], unique=False)
#     op.create_index(op.f('ix_module_analytics_module_id'), 'module_analytics', ['module_id'], unique=False)
#     op.create_index(op.f('ix_module_analytics_user_id'), 'module_analytics', ['user_id'], unique=False)
#     op.create_table('notifications',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('type', sa.String(length=50), nullable=False),
#     sa.Column('title', sa.String(length=255), nullable=False),
#     sa.Column('message', sa.Text(), nullable=False),
#     sa.Column('is_read', sa.Boolean(), nullable=True),
#     sa.Column('read_at', sa.DateTime(), nullable=True),
#     sa.Column('data', sa.JSON(), nullable=True),
#     sa.Column('action_url', sa.String(length=255), nullable=True),
#     sa.Column('priority', sa.String(length=20), nullable=True),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.Column('expires_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_notification_user_read', 'notifications', ['user_id', 'is_read'], unique=False)
#     op.create_index(op.f('ix_notifications_created_at'), 'notifications', ['created_at'], unique=False)
#     op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)
#     op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
#     op.create_table('otp_tokens',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('otp_hash', sa.String(length=255), nullable=False),
#     sa.Column('purpose', sa.String(length=50), nullable=False),
#     sa.Column('expires_at', sa.DateTime(), nullable=False),
#     sa.Column('used', sa.Boolean(), nullable=False),
#     sa.Column('attempts', sa.Integer(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_otp_user_purpose', 'otp_tokens', ['user_id', 'purpose'], unique=False)
#     op.create_index(op.f('ix_otp_tokens_expires_at'), 'otp_tokens', ['expires_at'], unique=False)
#     op.create_index(op.f('ix_otp_tokens_user_id'), 'otp_tokens', ['user_id'], unique=False)
#     op.create_table('sessions',
#     sa.Column('id', sa.String(length=36), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('refresh_token_hash', sa.String(length=255), nullable=False),
#     sa.Column('device_info', sa.String(length=255), nullable=True),
#     sa.Column('ip_address', sa.String(length=45), nullable=True),
#     sa.Column('expires_at', sa.DateTime(), nullable=False),
#     sa.Column('revoked', sa.Boolean(), nullable=False),
#     sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.Column('last_used_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('refresh_token_hash')
#     )
#     op.create_index('idx_session_user_active', 'sessions', ['user_id', 'revoked'], unique=False)
#     op.create_index(op.f('ix_sessions_expires_at'), 'sessions', ['expires_at'], unique=False)
#     op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
#     op.create_table('user_achievements',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('achievement_id', sa.Integer(), nullable=False),
#     sa.Column('awarded_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
#     sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('user_id', 'achievement_id', name='uq_user_achievement')
#     )
#     op.create_table('user_progression',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('total_xp', sa.Integer(), nullable=False),
#     sa.Column('level', sa.Integer(), nullable=False),
#     sa.Column('rank_title', sa.String(length=100), nullable=True),
#     sa.Column('streak_count', sa.Integer(), nullable=False),
#     sa.Column('last_activity_date', sa.DateTime(), nullable=True),
#     sa.Column('updated_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index(op.f('ix_user_progression_last_activity_date'), 'user_progression', ['last_activity_date'], unique=False)
#     op.create_index(op.f('ix_user_progression_user_id'), 'user_progression', ['user_id'], unique=True)
#     op.create_table('user_quests',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('quest_id', sa.Integer(), nullable=False),
#     sa.Column('status', sa.String(length=20), nullable=True),
#     sa.Column('progress', sa.Integer(), nullable=True),
#     sa.Column('completed_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['quest_id'], ['quests.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id'),
#     sa.UniqueConstraint('user_id', 'quest_id', name='uq_user_quest')
#     )
#     op.create_index('idx_user_quest_status', 'user_quests', ['user_id', 'status'], unique=False)
#     op.create_table('xp_transactions',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('user_id', sa.Integer(), nullable=False),
#     sa.Column('module_id', sa.Integer(), nullable=True),
#     sa.Column('xp_awarded', sa.Integer(), nullable=False),
#     sa.Column('source', sa.String(length=50), nullable=False),
#     sa.Column('reason', sa.String(length=255), nullable=True),
#     sa.Column('created_at', sa.DateTime(), nullable=True),
#     sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
#     sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_index('idx_xp_user_time', 'xp_transactions', ['user_id', 'created_at'], unique=False)
#     op.create_index(op.f('ix_xp_transactions_created_at'), 'xp_transactions', ['created_at'], unique=False)
#     op.create_index(op.f('ix_xp_transactions_source'), 'xp_transactions', ['source'], unique=False)
#     op.create_index(op.f('ix_xp_transactions_user_id'), 'xp_transactions', ['user_id'], unique=False)
#     # ### end Alembic commands ###


# def downgrade() -> None:
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.drop_index(op.f('ix_xp_transactions_user_id'), table_name='xp_transactions')
#     op.drop_index(op.f('ix_xp_transactions_source'), table_name='xp_transactions')
#     op.drop_index(op.f('ix_xp_transactions_created_at'), table_name='xp_transactions')
#     op.drop_index('idx_xp_user_time', table_name='xp_transactions')
#     op.drop_table('xp_transactions')
#     op.drop_index('idx_user_quest_status', table_name='user_quests')
#     op.drop_table('user_quests')
#     op.drop_index(op.f('ix_user_progression_user_id'), table_name='user_progression')
#     op.drop_index(op.f('ix_user_progression_last_activity_date'), table_name='user_progression')
#     op.drop_table('user_progression')
#     op.drop_table('user_achievements')
#     op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
#     op.drop_index(op.f('ix_sessions_expires_at'), table_name='sessions')
#     op.drop_index('idx_session_user_active', table_name='sessions')
#     op.drop_table('sessions')
#     op.drop_index(op.f('ix_otp_tokens_user_id'), table_name='otp_tokens')
#     op.drop_index(op.f('ix_otp_tokens_expires_at'), table_name='otp_tokens')
#     op.drop_index('idx_otp_user_purpose', table_name='otp_tokens')
#     op.drop_table('otp_tokens')
#     op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
#     op.drop_index(op.f('ix_notifications_is_read'), table_name='notifications')
#     op.drop_index(op.f('ix_notifications_created_at'), table_name='notifications')
#     op.drop_index('idx_notification_user_read', table_name='notifications')
#     op.drop_table('notifications')
#     op.drop_index(op.f('ix_module_analytics_user_id'), table_name='module_analytics')
#     op.drop_index(op.f('ix_module_analytics_module_id'), table_name='module_analytics')
#     op.drop_index(op.f('ix_module_analytics_event_type'), table_name='module_analytics')
#     op.drop_index(op.f('ix_module_analytics_created_at'), table_name='module_analytics')
#     op.drop_index('idx_module_event', table_name='module_analytics')
#     op.drop_table('module_analytics')
#     op.drop_index(op.f('ix_leaderboards_user_id'), table_name='leaderboards')
#     op.drop_index(op.f('ix_leaderboards_module_id'), table_name='leaderboards')
#     op.drop_index('idx_leaderboard_module_score', table_name='leaderboards')
#     op.drop_table('leaderboards')
#     op.drop_index(op.f('ix_game_sessions_user_id'), table_name='game_sessions')
#     op.drop_index(op.f('ix_game_sessions_module_id'), table_name='game_sessions')
#     op.drop_index('idx_game_user_module', table_name='game_sessions')
#     op.drop_table('game_sessions')
#     op.drop_index(op.f('ix_feedback_user_id'), table_name='feedback')
#     op.drop_table('feedback')
#     op.drop_index(op.f('ix_users_username'), table_name='users')
#     op.drop_index(op.f('ix_users_last_login_at'), table_name='users')
#     op.drop_index(op.f('ix_users_email'), table_name='users')
#     op.drop_table('users')
#     op.drop_index(op.f('ix_quests_module_id'), table_name='quests')
#     op.drop_table('quests')
#     op.drop_table('roles')
#     op.drop_index(op.f('ix_modules_slug'), table_name='modules')
#     op.drop_index('idx_module_type_active', table_name='modules')
#     op.drop_table('modules')
#     op.drop_table('achievements')
#     # ### end Alembic commands ###
