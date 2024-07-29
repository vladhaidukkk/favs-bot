"""Create update_wishes_updated_at trigger.

Revision ID: 085a4de99cfa
Revises: a437b2680ce5
Create Date: 2024-07-29 13:55:14.797742+00:00

"""

from typing import Sequence, Union

from alembic import op

revision: str = "085a4de99cfa"
down_revision: Union[str, None] = "a437b2680ce5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION update_wishes_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """        
        CREATE TRIGGER update_wishes_updated_at
        BEFORE UPDATE ON wishes
        FOR EACH ROW
        EXECUTE FUNCTION update_wishes_updated_at();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER update_wishes_updated_at ON wishes")
    op.execute("DROP FUNCTION update_wishes_updated_at()")
