"""_inventory_00006

Revision ID: 13adeaceee5f
Revises: 90565618a4b0
Create Date: 2022-12-26 00:47:33.759947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import sessionmaker
from api.config import settings
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '13adeaceee5f'
down_revision = '90565618a4b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_uuid',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('inventory_date', sa.Date(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('inventory_hibernate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('id_brand_brewing', sa.Integer(), nullable=False),
    sa.Column('tank_origin', sa.Integer(), nullable=False),
    sa.Column('tank_origin_level', sa.Integer(), nullable=False),
    sa.Column('tank_storage', sa.Integer(), nullable=False),
    sa.Column('tank_storage_level', sa.Integer(), nullable=False),
    sa.Column('tank_storage_og', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('tank_storage_abw', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('tank_storage_o2', sa.Integer(), nullable=True),
    sa.Column('note_origin', sa.String(length=256), nullable=True),
    sa.Column('tank_final', sa.Integer(), nullable=True),
    sa.Column('tank_final_level', sa.Integer(), nullable=True),
    sa.Column('note_final', sa.String(length=256), nullable=True),
    sa.Column('is_complete', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_brand_brewing'], ['brand_brewing.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uuid'], ['inventory_uuid.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory_last_brews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('bh_1', sa.String(length=16), nullable=True),
    sa.Column('bh_2', sa.String(length=16), nullable=True),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uuid'], ['inventory_uuid.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('inventory_hop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('id_commodity', sa.Integer(), nullable=False),
    sa.Column('final_boxes', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('final_pounds', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('final_total', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('lot_number', sa.String(), nullable=False),
    sa.Column('is_current', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_commodity'], ['commodity.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uuid'], ['inventory_uuid.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uuid'], ['inventory_last_brews.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory_material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('id_commodity', sa.Integer(), nullable=False),
    sa.Column('final_count', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('final_total', sa.Numeric(precision=9, scale=2), nullable=False),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_commodity'], ['commodity.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uuid'], ['inventory_uuid.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON inventory_uuid
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON inventory_hibernate
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON inventory_last_brews
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON inventory_hop
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON inventory_material
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE OR REPLACE FUNCTION delete_old_rows_inventory_uuid() RETURNS TRIGGER
    LANGUAGE plpgsql
    AS
    $$
    BEGIN
    DELETE FROM inventory_uuid WHERE time_created < NOW() - INTERVAL '1095 days';
    RETURN NULL;
    END;
    $$;
    """)
    session.execute("""
    CREATE TRIGGER trigger_delete_old_rows_inventory_uuid
    AFTER INSERT ON inventory_uuid
    EXECUTE PROCEDURE delete_old_rows_inventory_uuid();
    """)
    session.execute("""
    CREATE OR REPLACE FUNCTION update_is_complete_inventory_hibernate() RETURNS TRIGGER
    LANGUAGE plpgsql
    AS
    $$
    BEGIN
    IF NEW.tank_final IS NOT NULL AND NEW.tank_final_level IS NOT NULL THEN NEW.is_complete = TRUE;
    END IF;
    RETURN NEW;
    END;
    $$;
    """)
    session.execute("""
    CREATE TRIGGER update_is_complete_inventory_hibernate
    BEFORE UPDATE
    ON inventory_hibernate
    FOR EACH ROW
    EXECUTE PROCEDURE update_is_complete_inventory_hibernate();
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory_material')
    op.drop_table('inventory_hop')
    op.drop_table('inventory_last_brews')
    op.drop_table('inventory_hibernate')
    op.drop_table('inventory_uuid')

    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("DROP FUNCTION delete_old_rows_inventory_uuid();")
    session.execute("DROP FUNCTION update_is_complete_inventory_hibernate();")
    # ### end Alembic commands ###
