"""init

Revision ID: f21309d7b399
Revises: 
Create Date: 2024-12-02 09:09:33.843542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f21309d7b399'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budgets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('charges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('budget_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['budget_id'], ['budgets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('allocation_percentage', sa.Float(), nullable=False),
    sa.Column('budget_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['budget_id'], ['budgets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('revenues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('budget_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['budget_id'], ['budgets.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revenues')
    op.drop_table('persons')
    op.drop_table('charges')
    op.drop_table('budgets')
    # ### end Alembic commands ###