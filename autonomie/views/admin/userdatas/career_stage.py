# -*- coding: utf-8 -*-
# * Authors:
#       * MICHEAU Paul <paul@kilya.biz>
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
#

"""
Career stages administration tools
"""
import os
from pyramid.httpexceptions import HTTPFound
from autonomie.models.career_stage import CareerStage
from autonomie.views import BaseView
from autonomie.utils.widgets import Link
from autonomie.forms.admin.career_stage import get_career_stage_schema
from autonomie.views import render_api
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminEditView,
    AdminTreeMixin,
    BaseAdminAddView,
    BaseAdminDisableView,
)
from autonomie.views.admin.userdatas import (
    USERDATAS_URL,
    UserDatasIndexView,
)

CAREER_STAGE_URL = os.path.join(USERDATAS_URL, 'career_stage')
CAREER_STAGE_ITEM_URL = os.path.join(CAREER_STAGE_URL, '{id}')


class CareerStageListView(AdminCrudListView):
    """
    List of career stages entries
    """
    title = u"Configuration des étapes de parcours"
    description = u""
    route_name = CAREER_STAGE_URL
    columns = [u"Libellé", u"Statut associé", u"Entrée CAE ?", \
u"Contrat ?", u"Sortie ?"]

    item_route_name = CAREER_STAGE_ITEM_URL

    def stream_columns(self, career_stage):
        """
        Stream the table datas for the given item
        :param obj career_stage: The CareerStage object to stream
        :returns: List of labels
        """
        if career_stage.is_entree_cae:
            entree = u"<i class='glyphicon glyphicon-ok-sign'></i>"
        else:
            entree = ""
        if career_stage.is_contrat:
            contrat = u"<i class='glyphicon glyphicon-ok-sign'></i>"
        else:
            contrat = ""
        if career_stage.is_sortie:
            sortie = u"<i class='glyphicon glyphicon-ok-sign'></i>"
        else:
            sortie = ""
        return (
            career_stage.name,
            career_stage.cae_situation,
            entree,
            contrat,
            sortie,
        )

    def stream_actions(self, career_stage):
        """
        Stream the actions available for the given tva object
        :param obj tva: Tva instance
        :returns: List of 5-uples (url, label, title, icon, disable)
        """
        yield Link(
            self._get_item_url(career_stage),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if career_stage.active:
            yield Link(
                self._get_item_url(career_stage, action='disable'),
                label=u"Désactiver",
                title=u"L'étape n'apparaitra plus dans l'interface",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(career_stage, action='disable'),
                u"Activer",
                title=u"L'étape apparaitra plus dans l'interface",
                icon="fa fa-check",
            )

    def load_items(self):
        return CareerStage.query(include_inactive=True).all()

    def more_template_vars(self, result):
        result['nodata_msg'] = u"Aucune étape de parcours n'a été configurée"
        return result


class CareerStageDisableView(BaseAdminDisableView):
    """
    Disable view
    """
    route_name = CAREER_STAGE_ITEM_URL
    disable_msg = u"L'étape de parcours a bien été désactivée"
    enable_msg = u"L'étape de parcours a bien été activée"


class CareerStageEditView(BaseAdminEditView):
    """
    Edit view
    """
    route_name = CAREER_STAGE_ITEM_URL

    schema = get_career_stage_schema()
    factory = CareerStage
    title = u"Modifier"

    def submit_success(self, appstruct):
        old_products = []
        for product in self.context.products:
            if product.id not in [p.get('id') for p in appstruct['products']]:
                product.active = False
                old_products.append(product)
        model = self.schema.objectify(appstruct, self.context)
        model.products.extend(old_products)
        self.dbsession.merge(model)
        self.dbsession.flush()

        if self.msg:
            self.request.session.flash(self.msg)

        return self.redirect()


class CareerStageAddView(BaseAdminAddView):
    """
    Add view
    """
    route_name = CAREER_STAGE_URL
    schema = get_career_stage_schema()
    factory = CareerStage
    title = u"Ajouter"


def includeme(config):
    """
    Add routes and views
    """
    config.add_route(CAREER_STAGE_URL, CAREER_STAGE_URL)
    config.add_route(CAREER_STAGE_ITEM_URL, CAREER_STAGE_ITEM_URL, \
traverse="/career_stage/{id}")

    config.add_admin_view(
        CareerStageListView,
        parent=UserDatasIndexView,
        renderer='admin/crud_list.mako',
    )
    config.add_admin_view(
        CareerStageDisableView,
        parent=CareerStageListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        CareerStageAddView,
        parent=CareerStageListView,
        request_param="action=add",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        CareerStageEditView,
        parent=CareerStageListView,
        renderer='admin/crud_add_edit.mako',
    )
