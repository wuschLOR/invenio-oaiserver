# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Models for storing information about OAIServer state."""

from flask_babelex import lazy_gettext as _
from invenio_db import db
from sqlalchemy.event import listen
from sqlalchemy_utils import Timestamp

from .proxies import current_oaiserver


class OAISet(db.Model, Timestamp):
    """Information about OAI set."""

    __tablename__ = 'oaiserver_set'

    id = db.Column(db.Integer, primary_key=True)

    spec = db.Column(
        db.String(40),
        nullable=False,
        unique=True,
        info=dict(
            label=_('Identifier'),
            description=_('Identifier of the set.'),
        )
    )
    """Set identifier."""

    name = db.Column(
        db.String(40),
        info=dict(
            label=_('Long name'),
            description=_('Long name of the set.'),
        )
    )
    """Human readable name of the set."""

    description = db.Column(
        db.Text,
        nullable=True,
        info=dict(
            label=_('Description'),
            description=_('Description of the set.'),
        ),
    )
    """Human readable description."""

    search_pattern = db.Column(
        db.Text,
        nullable=True,
        info=dict(
            label=_('Search pattern'),
            description=_('Search pattern to select records'),
        )
    )
    """Search pattern to get records."""


def oaiset_removed_or_inserted(mapper, connection, target):
    """Invalidate cache on collection insert or delete."""
    current_oaiserver.sets = None


def oaiset_attribute_changed(target, value, oldvalue, initiator):
    """Invalidate cache if dbquery change."""
    if value != oldvalue:
        current_oaiserver.sets = None


# update cache with list of collections
listen(OAISet, 'after_insert', oaiset_removed_or_inserted)
listen(OAISet, 'after_delete', oaiset_removed_or_inserted)
listen(OAISet.search_pattern, 'set', oaiset_attribute_changed)

__all__ = ('OAISet', )
