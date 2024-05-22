"""empty message

Revision ID: 00bd959266d8
Revises: 0e97c67391c6
Create Date: 2024-05-22 11:49:31.425960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00bd959266d8'
down_revision = '0e97c67391c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('approvisionnement',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('produit_id', sa.Integer(), nullable=False),
    sa.Column('qte_actuelle', sa.Integer(), nullable=False),
    sa.Column('qte_ajoutee', sa.Integer(), nullable=False),
    sa.Column('date_heure', sa.DateTime(), nullable=False),
    sa.Column('montant', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['produit_id'], ['produit.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('approvisionnement')
    # ### end Alembic commands ###
