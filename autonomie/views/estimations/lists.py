# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import logging
import colander
from sqlalchemy import (distinct, extract)
from sqlalchemy.orm import (
    contains_eager,
    load_only,
)

from autonomie.forms.tasks.estimation import (
    get_list_schema,
)

from autonomie.models.company import Company
from autonomie.models.customer import Customer
from autonomie.models.task import (
    Estimation,
    Task,
)
from autonomie.views import (
    BaseListView,
)


logger = logging.getLogger(__name__)


class GlobalEstimationList(BaseListView):
    title = u"Devis de la CAE"
    add_template_vars = (u'title', 'is_admin', 'legends')
    schema = get_list_schema(is_global=True, excludes=('status',))
    sort_columns = dict(
        date=Estimation.date,
        customer=Customer.label,
        company=Company.name,
    )
    default_sort = 'date'
    default_direction = 'desc'
    is_admin = True
    legends = (
        ('geninv-True', u"Devis concrétisés en facture"),
		('signed-status-signed', u"Devis signés"),
        ("", u"Devis en cours"),
        ("signed-status-aborted", u"Devis sans suite"),
    )

    def query(self):
        query = self.request.dbsession.query(
            distinct(Estimation.id),
            Estimation,
        )
        query = query.outerjoin(Task.company)
        query = query.outerjoin(Task.customer)
        query = query.options(
            contains_eager(Task.customer).load_only(
                Customer.id,
                Customer.label,
            )
        )
        query = query.options(
            contains_eager(Task.company).load_only(
                Company.id,
                Company.name
            )
        )
        query = query.options(
            load_only(
                "name",
                "internal_number",
                "status",
                "signed_status",
                "geninv",
                "date",
                "description",
                "ht",
                "tva",
                "ttc",
            )
        )
        return query

    def filter_date(self, query, appstruct):
        period = appstruct.get('period', {})
        if period.get('start') not in (colander.null, None):
            logger.debug("  + Filtering by date : %s" % period)
            start = period.get('start')
            end = period.get('end')
            if end not in (None, colander.null):
                end = datetime.date.today()
            query = query.filter(Task.date.between(start, end))
        else:
            year = appstruct.get('year')
            if year is not None:
                query = query.filter(extract('year', Estimation.date) == year)
        return query

    def filter_ttc(self, query, appstruct):
        ttc = appstruct.get('ttc', {})
        if ttc.get('start') not in (None, colander.null):
            logger.info(u"  + Filtering by ttc amount : %s" % ttc)
            start = ttc.get('start')
            end = ttc.get('end')
            if end in (None, colander.null):
                query = query.filter(Estimation.ttc >= start)
            else:
                query = query.filter(Estimation.ttc.between(start, end))
        return query

    def _get_company_id(self, appstruct):
        return appstruct.get('company_id')

    def filter_company(self, query, appstruct):
        company_id = self._get_company_id(appstruct)
        if company_id not in (None, colander.null):
            logger.info("  + Filtering on the company id : %s" % company_id)
            query = query.filter(Task.company_id == company_id)
        return query

    def filter_customer(self, query, appstruct):
        """
            filter estimations by customer
        """
        customer_id = appstruct.get('customer_id')
        if customer_id not in (None, colander.null):
            logger.info("  + Filtering on the customer id : %s" % customer_id)
            query = query.filter(Estimation.customer_id == customer_id)
        return query

    def filter_signed_status(self, query, appstruct):
        """
        Filter estimations by signed status
        """
        status = appstruct['signed_status']
        logger.info("  + Signed status filtering : %s" % status)
        if status == 'geninv':
            query = query.filter(Estimation.geninv == True)
        elif status != 'all':
            query = query.filter(Estimation.signed_status == status)

        return query

    def filter_status(self, query, appstruct):
        """
        Filter the estimations by status
        """
        query = query.filter(Estimation.status == 'valid')
        return query

    def more_template_vars(self, response_dict):
        """
        Add template vars to the response dict

        :param obj result: A Sqla Query
        :returns: vars to pass to the template
        :rtype: dict
        """
        ret_dict = BaseListView.more_template_vars(self, response_dict)
        records = response_dict['records']
        # Les records sont des 2-uples (identifiant, instance)
        ret_dict['totalht'] = sum(r[1].ht for r in records)
        ret_dict['totaltva'] = sum(r[1].tva for r in records)
        ret_dict['totalttc'] = sum(r[1].ttc for r in records)
        return ret_dict


class CompanyEstimationList(GlobalEstimationList):
    is_admin = False
    schema = get_list_schema(is_global=False, excludes=("company_id",))
    add_template_vars = (u'title', 'is_admin', "with_draft", 'legends')
    legends = GlobalEstimationList.legends + (
		('status-draft', u"Devis en brouillon"),
        ('status-wait', u"Devis en attente de validation"),
        ('status-invalid', u"Devis invalides"),
    )

    @property
    def with_draft(self):
        return True

    @property
    def title(self):
        return u"Devis de l'entreprise {0}".format(
            self.request.context.name
        )

    def _get_company_id(self, appstruct):
        """
        Return the current context's company id
        """
        return self.request.context.id

    def filter_status(self, query, appstruct):
        """
        Filter the estimations by status
        """
        status = appstruct.get('status', 'all')
        logger.info("  + Status filtering : %s" % status)
        if status != 'all':
            query = query.filter(Estimation.status == status)

        return query


def add_routes(config):
    """
    Add module's specific routes
    """
    config.add_route(
        "company_estimations",
        "/company/{id:\d+}/estimations",
        traverse="/companies/{id}"
    )
    config.add_route(
        "estimations",
        "/estimations",
    )


def add_views(config):
    """
    Add the views defined in this module
    """
    # Estimation list related views
    config.add_view(
        CompanyEstimationList,
        route_name="company_estimations",
        renderer="estimations.mako",
        permission="list_estimations",
    )

    config.add_view(
        GlobalEstimationList,
        route_name="estimations",
        renderer="estimations.mako",
        permission="admin_tasks",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
