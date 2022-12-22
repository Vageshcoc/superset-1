# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""add_unique_name_desc_rls

Revision ID: f3afaf1f11f0
Revises: e09b4ae78457
Create Date: 2022-06-19 16:17:23.318618

"""

# revision identifiers, used by Alembic.
revision = "f3afaf1f11f0"
down_revision = "e09b4ae78457"

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class RowLevelSecurityFilter(Base):
    __tablename__ = "row_level_security_filters"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), unique=True, nullable=False)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)

    op.add_column(
        "row_level_security_filters", sa.Column("name", sa.String(length=255))
    )
    op.add_column(
        "row_level_security_filters", sa.Column("description", sa.Text(), nullable=True)
    )

    # Set initial default names make sure we can have unique non null values
    all_rls = session.query(RowLevelSecurityFilter).all()
    for rls in all_rls:
        rls.name = f"rls-{rls.id}"
    session.commit()

    # Now it's safe so set non-null and unique
    # add unique constraint
    with op.batch_alter_table("row_level_security_filters") as batch_op:
        # batch mode is required for sqlite
        batch_op.alter_column(
            "name",
            existing_type=sa.String(255),
            nullable=False,
        )
        batch_op.create_unique_constraint("uq_rls_name", ["name"])
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table("row_level_security_filters") as batch_op:
        batch_op.drop_constraint("uq_rls_name", type_="unique")
        batch_op.drop_column("description")
        batch_op.drop_column("name")