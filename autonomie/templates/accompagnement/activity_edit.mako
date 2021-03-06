<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="definition_list" />
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name='afteractionmenu'>
<% activity = request.context %>
<% pdf_url = request.route_path("activity.pdf", id=activity.id) %>
    % if activity.status != 'planned':
    <a
        class='btn btn-default pull-right'
        href='${pdf_url}'
        >
        <i class='glyphicon glyphicon-file'></i>Voir le PDF
    </a>
    % endif
</%block>
<%block name="content">
<% activity = request.context %>
<div class='row'>
    <div class='col-md-4'>
        <div class='panel panel-default page-block'>
            <div class='panel-heading'>
            Informations générales
            </div>
            <div class='panel-body'>
            <% companies = set() %>
                <h3>Participants</h3>
                <ul>
                % for participant in activity.participants:
                    <li>
                    <% url = request.route_path("/users/{id}", id=participant.id) %>
                    <a href='#' onclick="window.openPopup('${url}');" >
                    ${api.format_account(participant)}</a> : ${ format_mail(participant.email) }
                    </li>
                    % for company in participant.companies:
                        <% companies.add(company) %>
                    % endfor
                %endfor
                </ul>
                <h3>Activités</h3>
                % for company in companies:
                    <div>
                        <b>${company.name}</b>
                        <ul>
                        % for label, route in ( \
                        (u'Liste des factures', 'company_invoices'), \
                        (u'Liste des devis', 'estimations'), \
                            (u'Gestion commerciale', 'commercial_handling'), \
                            ):
                            <li>
                                <% url = request.route_path(route, id=company.id) %>
                                <a href='#' onclick='window.openPopup("${url}");'>${label}</a>
                            </li>
                        % endfor
                        </ul>
                    </div>
                % endfor
                <strong>Fichiers attachés</strong>
                <div>
                    ${format_filelist(activity)}
                </div>
                <% resulting_companies = set(activity.companies).difference(companies) %>
                % if resulting_companies:
                    <strong>Autres entreprises concernées</strong>
                    % for company in resulting_companies:
                        <div>
                            <a href="${request.route_path('company', id=company.id)}">
                                ${company.name}
                            </a>
                        </div>
                    % endfor
                % endif
            </div>
        </div>
    </div>
    <div class='col-md-8'>
            <div class='panel panel-default page-block'>
            <div class='panel-heading'>
                Configuration du rendez-vous
            </div>
            <div class='panel-body'>
                <% items = (\
                (u'Conseiller(s)', ', '.join([api.format_account(conseiller) for conseiller in activity.conseillers])), \
                    (u'Horaire', api.format_datetime(activity.datetime)), \
                    (u'Action', u"%s %s" % (activity.action_label, activity.subaction_label)), \
                    (u"Nature du rendez-vous", activity.type_object.label), \
                    (u"Mode d'entretien", activity.mode), \
                    )\
                %>
                <div class='row'>
                    <div class='col-md-7'>
                        ${definition_list(items)}
                    </div>
                    <div class='col-md-5'>
                        <div class='btn-group'>
                        <button
                            class='btn btn-default'
                            data-toggle='collapse'
                            data-target='#edition_form'
                            title="Modifier ce rendez-vous"
                            >
                            <i class='fa fa-pencil'></i>&nbsp;Modifier
                        </button>
                        <button
                            class="btn btn-primary"
                            data-toggle='collapse'
                            data-target='#next_activity_form_container'
                            title="Programmer un nouveau rendez-vous"
                            >
                            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Nouveau rendez-vous
                        </button>
                        </div>
                    </div>
                </div>
            </div>

                <div
                    % if formerror is not UNDEFINED:
                        class='section-content'
                    % else:
                        class='section-content collapse'
                    % endif
                    id='edition_form'>
                    <button class="close" data-toggle="collapse" data-target='#edition_form' type="button">×</button>
                    ${form|n}
                </div>
                <div class='section-content collapse' id='next_activity_form_container'>
                    <button class="close" data-toggle="collapse" data-target='#next_activity_form_container' type="button">×</button>
                    <div id="next_activity_message"></div>
                    ${next_activity_form|n}
                </div>
            </div>
            <div class='panel panel-default page-block'>
                <div class='panel-heading'>
                    Saisie des données
                </div>
                <div class='panel-body'>
                    ${record_form|n}
                </div>
                </div>
            </div>
            </div>
    </div>
</div>
</%block>
<%block name="footerjs">
<% activity = request.context %>
<% pdf_url = request.route_path("activity.pdf", id=activity.id) %>
setAuthCheckBeforeSubmit('#record_form');
if (window.location.search.indexOf("show=pdf") != -1){
window.open("${pdf_url}");
}
</%block>
