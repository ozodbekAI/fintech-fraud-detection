"""create

Revision ID: 2df420944057
Revises: 1a198b68bc4a
Create Date: 2025-09-20 14:55:08.237540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2df420944057'
down_revision: Union[str, Sequence[str], None] = '1a198b68bc4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
