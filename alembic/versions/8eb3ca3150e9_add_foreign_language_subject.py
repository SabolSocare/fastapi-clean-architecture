"""add_foreign_language_subject

Revision ID: 8eb3ca3150e9
Revises: cad0cdcb0e2d
Create Date: 2025-12-28 00:04:32.481210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eb3ca3150e9'
down_revision: Union[str, None] = 'cad0cdcb0e2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add foreign language score and max columns
    op.add_column('students', sa.Column('foreign_language_score', sa.Float(), nullable=False, server_default='0.0'))
    op.add_column('students', sa.Column('foreign_language_max', sa.Float(), nullable=False, server_default='50.0'))


def downgrade() -> None:
    # Remove foreign language columns
    op.drop_column('students', 'foreign_language_max')
    op.drop_column('students', 'foreign_language_score')
