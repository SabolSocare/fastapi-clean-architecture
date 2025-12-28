"""swap_khmer_math_max_scores

Revision ID: cad0cdcb0e2d
Revises: 77fb52a63678
Create Date: 2025-12-27 23:59:39.887462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cad0cdcb0e2d'
down_revision: Union[str, None] = '77fb52a63678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update default max scores: Khmer 75 -> 125, Math 125 -> 75
    op.execute("ALTER TABLE students ALTER COLUMN khmer_max SET DEFAULT 125.0")
    op.execute("ALTER TABLE students ALTER COLUMN math_max SET DEFAULT 75.0")
    
    # Update existing records to new max scores
    op.execute("UPDATE students SET khmer_max = 125.0 WHERE khmer_max = 75.0")
    op.execute("UPDATE students SET math_max = 75.0 WHERE math_max = 125.0")


def downgrade() -> None:
    # Revert to old max scores: Khmer 125 -> 75, Math 75 -> 125
    op.execute("ALTER TABLE students ALTER COLUMN khmer_max SET DEFAULT 75.0")
    op.execute("ALTER TABLE students ALTER COLUMN math_max SET DEFAULT 125.0")
    
    # Revert existing records
    op.execute("UPDATE students SET khmer_max = 75.0 WHERE khmer_max = 125.0")
    op.execute("UPDATE students SET math_max = 125.0 WHERE math_max = 75.0")
