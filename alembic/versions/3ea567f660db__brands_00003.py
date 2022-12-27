"""_brands_00003

Revision ID: 3ea567f660db
Revises: d6931db81268
Create Date: 2022-12-16 17:59:48.493321

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from api.config import settings
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '3ea567f660db'
down_revision = 'd6931db81268'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand_brewing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_brand', sa.String(length=4), unique=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('is_organic', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('is_dryhop', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('is_addition', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brand_finishing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_brand_brewing', sa.Integer(), nullable=False),
    sa.Column('name_brand', sa.String(length=4), unique=True, nullable=False),
    sa.Column('is_preinjection', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('is_postinjection', sa.Boolean(), server_default=sa.text('True'), nullable=False),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_brand_brewing'], ['brand_brewing.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brand_packaging',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_brand_finishing', sa.Integer(), nullable=False),
    sa.Column('name_brand', sa.String(length=4), unique=True, nullable=False),
    sa.Column('note', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_brand_finishing'], ['brand_finishing.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON brand_brewing
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON brand_finishing
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    session.execute("""
    CREATE TRIGGER update_timestamp
    BEFORE UPDATE
    ON brand_packaging
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('brand_packaging')
    op.drop_table('brand_finishing')
    op.drop_table('brand_brewing')
    # ### end Alembic commands ###