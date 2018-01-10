"""empty message

Revision ID: 04537ae40768
Revises: 809b49633a03
Create Date: 2017-04-05 13:00:44.107520

"""

# revision identifiers, used by Alembic.
revision = '04537ae40768'
down_revision = '809b49633a03'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('membership_roles',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deleted', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_memberships',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('org_user_role_id', sa.Integer(), nullable=True),
    sa.Column('street', sa.String(length=255), nullable=True),
    sa.Column('zip', sa.String(length=25), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('deleted', sa.Integer(), nullable=True),
    sa.Column('ts_deleted', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['org_user_role_id'], ['membership_roles.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('organization_user_roles')
    op.drop_table('organizations_users')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organizations_users',
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('organization_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('org_user_role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('street', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('zip', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('comment', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('ts_deleted', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['org_user_role_id'], ['organization_user_roles.id'], name='organizations_users_org_user_role_id_fkey'),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], name='organizations_users_organization_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='organizations_users_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='organizations_users_pkey')
    )
    op.create_table('organization_user_roles',
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('deleted', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('display_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='organization_user_roles_pkey')
    )
    op.drop_table('organization_memberships')
    op.drop_table('membership_roles')
    ### end Alembic commands ###
