"""add_user_system

Revision ID: f59716b84cde
Revises:
Create Date: 2026-04-27 18:04:04.892927

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'f59716b84cde'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(conn, name: str) -> bool:
    return inspect(conn).has_table(name)


def _column_exists(conn, table: str, column: str) -> bool:
    cols = [c["name"] for c in inspect(conn).get_columns(table)]
    return column in cols


def _constraint_exists(conn, table: str, constraint_name: str) -> bool:
    """Check if a named constraint exists (works for PostgreSQL)."""
    try:
        ucs = inspect(conn).get_unique_constraints(table)
        return any(uc["name"] == constraint_name for uc in ucs)
    except Exception:
        return False


def upgrade() -> None:
    conn = op.get_bind()
    is_pg = conn.dialect.name == "postgresql"

    # ── users ──────────────────────────────────────────────────────────────────
    if not _table_exists(conn, "users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("display_name", sa.String(length=100), nullable=False),
            sa.Column("hashed_password", sa.String(length=255), nullable=False),
            sa.Column("subscription_tier", sa.String(length=20), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("last_login", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── gedaechtnis_scores ─────────────────────────────────────────────────────
    if not _table_exists(conn, "gedaechtnis_scores"):
        op.create_table(
            "gedaechtnis_scores",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("game_type", sa.String(length=50), nullable=False),
            sa.Column("score", sa.Integer(), nullable=False),
            sa.Column("player_name", sa.String(length=50), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_gedaechtnis_scores_user_id"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_gedaechtnis_scores_game_type", "gedaechtnis_scores", ["game_type"])
        op.create_index("ix_gedaechtnis_scores_user_id", "gedaechtnis_scores", ["user_id"])

    # ── game_sessions: add user_id ─────────────────────────────────────────────
    if not _column_exists(conn, "game_sessions", "user_id"):
        if is_pg:
            op.add_column("game_sessions", sa.Column("user_id", sa.Integer(), nullable=True))
            op.create_index("ix_game_sessions_user_id", "game_sessions", ["user_id"])
            op.create_foreign_key("fk_game_sessions_user_id", "game_sessions", "users", ["user_id"], ["id"])
        else:
            with op.batch_alter_table("game_sessions") as batch_op:
                batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
                batch_op.create_index("ix_game_sessions_user_id", ["user_id"])
                batch_op.create_foreign_key("fk_game_sessions_user_id", "users", ["user_id"], ["id"])

    # ── user_achievements: add user_id + drop old slug-unique + composite unique
    if not _column_exists(conn, "user_achievements", "user_id"):
        if is_pg:
            op.add_column("user_achievements", sa.Column("user_id", sa.Integer(), nullable=True))
            op.create_index("ix_user_achievements_user_id", "user_achievements", ["user_id"])
            # Drop old single-column unique before adding composite unique
            op.drop_constraint("user_achievements_slug_key", "user_achievements", type_="unique")
            op.create_unique_constraint("uq_achievement_slug_user", "user_achievements", ["slug", "user_id"])
            op.create_foreign_key("fk_user_achievements_user_id", "user_achievements", "users", ["user_id"], ["id"])
        else:
            with op.batch_alter_table("user_achievements") as batch_op:
                batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
                batch_op.create_index("ix_user_achievements_user_id", ["user_id"])
                batch_op.create_unique_constraint("uq_achievement_slug_user", ["slug", "user_id"])

    # ── user_progress: add user_id + drop old game_type-unique + composite unique
    if not _column_exists(conn, "user_progress", "user_id"):
        if is_pg:
            op.add_column("user_progress", sa.Column("user_id", sa.Integer(), nullable=True))
            op.create_index("ix_user_progress_user_id", "user_progress", ["user_id"])
            # Drop old single-column unique before adding composite unique
            op.drop_constraint("user_progress_game_type_key", "user_progress", type_="unique")
            op.create_unique_constraint("uq_progress_game_user", "user_progress", ["game_type", "user_id"])
            op.create_foreign_key("fk_user_progress_user_id", "user_progress", "users", ["user_id"], ["id"])
        else:
            with op.batch_alter_table("user_progress") as batch_op:
                batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
                batch_op.create_index("ix_user_progress_user_id", ["user_id"])
                batch_op.create_unique_constraint("uq_progress_game_user", ["game_type", "user_id"])


def downgrade() -> None:
    conn = op.get_bind()
    is_pg = conn.dialect.name == "postgresql"

    if is_pg:
        op.drop_constraint("fk_user_progress_user_id", "user_progress", type_="foreignkey")
        op.drop_constraint("uq_progress_game_user", "user_progress", type_="unique")
        op.drop_index("ix_user_progress_user_id", table_name="user_progress")
        op.drop_column("user_progress", "user_id")

        op.drop_constraint("fk_user_achievements_user_id", "user_achievements", type_="foreignkey")
        op.drop_constraint("uq_achievement_slug_user", "user_achievements", type_="unique")
        op.drop_index("ix_user_achievements_user_id", table_name="user_achievements")
        op.drop_column("user_achievements", "user_id")

        op.drop_constraint("fk_game_sessions_user_id", "game_sessions", type_="foreignkey")
        op.drop_index("ix_game_sessions_user_id", table_name="game_sessions")
        op.drop_column("game_sessions", "user_id")
    else:
        with op.batch_alter_table("user_progress") as batch_op:
            batch_op.drop_constraint("uq_progress_game_user", type_="unique")
            batch_op.drop_index("ix_user_progress_user_id")
            batch_op.drop_column("user_id")
        with op.batch_alter_table("user_achievements") as batch_op:
            batch_op.drop_constraint("uq_achievement_slug_user", type_="unique")
            batch_op.drop_index("ix_user_achievements_user_id")
            batch_op.drop_column("user_id")
        with op.batch_alter_table("game_sessions") as batch_op:
            batch_op.drop_index("ix_game_sessions_user_id")
            batch_op.drop_column("user_id")
