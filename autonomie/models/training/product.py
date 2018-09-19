# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * BODRERO Sébastien <bodrero.sebastien@gmail.com>
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
    Training product model : represents trainings product
"""

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    Table,
    String,
    Float,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.compute.math_utils import integer_to_amount
from autonomie import forms
from autonomie.forms.custom_types import AmountType

TRAINING_PRODUCT_TO_GROUP_REL_TABLE = Table(
    "training_product_product_group_rel",
    DBBASE.metadata,
    Column(
        "traiing_sale_product_id",
        Integer,
        ForeignKey('training_sale_product.id', ondelete='cascade')
    ),
    Column(
        "training_sale_product_group_id",
        Integer,
        ForeignKey(
            'training_sale_product_group.id',
            ondelete='cascade',
            name="fk_training_product_to_group_rel_group_id"
        )
    ),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class TrainingSaleProductCategory(DBBASE):
    """
    A training product category allowing to group training
    :param id: unique id
    :param title: the title of the category
    :param description: the training category description
    :param company_id: company that owns the category
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    title = Column(
        String(255),
        nullable=False,
        info={
            "colanderalchemy": {'title': u"Titre"}
        }
    )
    description = Column(Text(), default="")
    company_id = Column(
        ForeignKey('company.id'),
        info={
            'export': {'exclude': True},
        }
    )
    company = relationship(
        "Company",
        info={
            'export': {'exclude': True},
        }
    )

    def __json__(self, request):
        """
        Json repr of our model
        """
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            company_id=self.company_id,
            product_groups=[item.__json__(request)
                            for item in self.product_groups],
            products=[item.__json__(request)
                      for item in self.products],
        )


class SaleProduct(DBBASE):
    """
    Training model
    Stores company trainings
    :param id: unique id
    :param title: title of the training item
    :param goals: goals of title of the training item
    :param prerequisites: prerequisites to subscribe to the training session
    :param for_who: target of the training item
    :param duration: duration of the training item
    :param content: content of the training item
    :param teaching_method: teaching_method used in training session
    :param logistics_means: logistics_means implemented for the training session
    :param more_stuff: Les plus...
    :param evaluation: evaluation criteria
    :param place: place if the training session
    :param modality: modality of the training session
    :param type: type of the training
    :param date: date og the training session
    :param price: price of the training session
    :param free_1: free input
    :param free_2: free input
    :param free_3: free input
    :param company_id: company that owns the training
    """
    __table_args__ = default_table_args
    __tablename__ = 'training_sale_product'
    id = Column(Integer, primary_key=True)

    title = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Intitulé",
            }
        },
        nullable=False,
        default=u''
    )

    goals = Column(
        String(10),
        info={
            'colanderalchemy': {
                'title': u"Objectifs à atteindre à l'issue de la formation",
            }
        },
        default=u'Les objectifs doivent être obligatoirement décrit avec des verbes d\'actions',
    )

    prerequisites = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Pré-requis obligatoire de la formation",
            }
        },
        default=u''
    )

    for_who = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Pour qui?",
            }
        },
        default=u'Public susceptible de participer à cette formation'
    )

    duration = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Durée en heures et en jour(s) pour la formation",
            }
        },
        nullable=False,
        default=u'Public susceptible de participer à cette formation'
    )

    content = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Contenu détaillé de la formation",
            }
        },
        default=u'trame par étapes'
    )

    teaching_method = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Les moyens pédagogiques utilisés",
            }
        },
        default=u''
    )

    logistics_means = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Moyens logistiques",
            }
        },
        default=u''
    )

    more_stuff = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Quels sont les plus de cette formation ?",
            }
        },
        default=u''
    )

    evaluation = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Modalités d'évaluation de la formation",
            }
        },
        default=u'Par exemple : questionnaire d\'évaluation, exercices-tests, questionnaire de satisfaction, '
                u'évaluation formative,... '
    )

    place = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Lieu de la formation",
            }
        },
        default=u'Villes, zones géographiques où la formation peut être mise en place'
    )

    modality = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Modalité de formation",
            }
        },
        default=u''
    )

    type = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Modalité de formation",
            }
        },
        default=u''
    )

    date = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Dates de la formation",
            }
        },
        default=u''
    )

    price = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Tarif de la formation",
            }
        },
        default=u''
    )

    free_1 = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Champ libre 1",
            }
        },
        default=u''
    )

    free_2 = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Champ libre 2",
            }
        },
        default=u''
    )

    free_3 = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u"Champ libre 3",
            }
        },
        default=u''
    )

    category_id = Column(ForeignKey('training_sale_product_category.id'))
    category = relationship(
        TrainingSaleProductCategory,
        backref=backref('products'),
        info={'colanderalchemy': forms.EXCLUDED},
    )

    def __json__(self, request):
        """
        Json repr of our model
        """
        return dict(
            id=self.id,
            title=self.title,
            goals=self.goals,
            prerequisites=self.prerequisites,
            for_who=self.for_who,
            duration=self.duration,
            content=self.content,
            teaching_method=self.teaching_method,
            logistics_means=self.logistics_means,
            more_stuff=self.more_stuff,
            evaluation=self.evaluation,
            place=self.place,
            modality=self.modality,
            type=self.type,
            date=self.date,
            price=self.price,
            free_1=self.free_1,
            free_2=self.free_2,
            free_3=self.free_3,
            category_id=self.category_id,
            category=self.category.title,
        )

    @property
    def company(self):
        return self.category.company