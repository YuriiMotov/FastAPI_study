"""orm-style and common metadata

Revision ID: db93610d9fc3
Revises: a98310137da9
Create Date: 2023-10-17 16:23:14.628964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'db93610d9fc3'
down_revision: Union[str, None] = 'a98310137da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('operation', 'quantity',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('operation', 'figi',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('operation', 'date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('operation', 'type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('operation', 'type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('operation', 'date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('operation', 'figi',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('operation', 'quantity',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
