"""remove model duplicating and switch to orm-style

Revision ID: de214cc4308c
Revises: 068fe04fb331
Create Date: 2023-10-05 11:19:41.590313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de214cc4308c'
down_revision: Union[str, None] = '068fe04fb331'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.alter_column('user', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('user', 'registered_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
