"""Run Alembic migrations programmatically.

Usage:
    set PYTHONPATH=.
    python run_migrations.py
"""
import os
import sys
from alembic.config import Config
from alembic import command

ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault('PYTHONPATH', ROOT)

def main():
    cfg = Config('alembic.ini')
    cfg.set_main_option('script_location', 'migrations')
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        cfg.set_main_option('sqlalchemy.url', database_url)
    
    try:
        print('Running alembic upgrade head...')
        command.upgrade(cfg, 'head')
        print('✓ Upgrade completed successfully')
    except Exception as e:
        print('✗ Upgrade failed:', str(e))
        raise

if __name__ == '__main__':
    main()

