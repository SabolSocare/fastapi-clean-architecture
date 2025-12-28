"""add student model

Revision ID: add_student_model
Revises: 490858f0a1a0
Create Date: 2025-01-15 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'add_student_model'
down_revision: Union[str, None] = '490858f0a1a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE genderenum AS ENUM ('M', 'F')")
    op.execute("CREATE TYPE gradeenum AS ENUM ('A', 'B', 'C', 'D', 'E', 'F')")
    
    # Create students table
    op.create_table('students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('gender', postgresql.ENUM('M', 'F', name='genderenum', create_type=False), nullable=False),
        sa.Column('khmer_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('math_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('history_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('geography_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('ethics_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('earth_science_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('khmer_max', sa.Float(), nullable=True, server_default='125.0'),
        sa.Column('math_max', sa.Float(), nullable=True, server_default='75.0'),
        sa.Column('history_max', sa.Float(), nullable=True, server_default='75.0'),
        sa.Column('geography_max', sa.Float(), nullable=True, server_default='75.0'),
        sa.Column('ethics_max', sa.Float(), nullable=True, server_default='75.0'),
        sa.Column('earth_science_max', sa.Float(), nullable=True, server_default='50.0'),
        sa.Column('total_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('average_score', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('grade', postgresql.ENUM('A', 'B', 'C', 'D', 'E', 'F', name='gradeenum', create_type=False), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_table('students')
    
    # Drop enum types
    op.execute('DROP TYPE IF EXISTS gradeenum')
    op.execute('DROP TYPE IF EXISTS genderenum')

