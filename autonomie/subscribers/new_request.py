# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
"""
Log all incoming requests
"""
import logging

from pyramid.events import NewRequest

from autonomie.utils.widgets import (
    ActionMenu,
    Navigation,
)
from autonomie.i18n import translate

logger = logging.getLogger(__name__)


def log_request(event):
    """
        Log each request
    """
    logger.info(u"####################  NEW REQUEST COMING #################")
    logger.info(u"  + The request object")
    result = event.request.as_bytes(skip_body=True).decode('utf-8')
    result += u"\n\n# Paramètres GET de la requête #\n"
    for key, value in event.request.GET.items():
        if key == "password":
            value = u"*************"
        result += u"{} : {}\n".format(key, value)
    result += u"# Paramètres POST de la requête #\n"
    for key, value in event.request.POST.items():
        if key == "password":
            value = u"*************"
        result += u"{} : {}\n".format(key, value)
    logger.info(result)
    logger.info(u"  + The session object")
    logger.info(event.request.session)
    logger.info(u"################### END REQUEST METADATA LOG #############")


def add_request_attributes(event):
    """
        Add usefull tools to the request object
        that may be used inside the views
    """
    request = event.request
    request.translate = translate
    # Old stuff will be deprecated with the time
    request.actionmenu = ActionMenu()
    # Use this one instead
    request.navigation = Navigation()
    request.popups = {}
    if request.params.get('popup', "") != "":
        logger.info("Relative window is a popup")
        request.is_popup = True
    else:
        request.is_popup = False


def includeme(config):
    config.add_subscriber(log_request, NewRequest)
    config.add_subscriber(add_request_attributes, NewRequest)
