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
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="format_text"/>
<%namespace file="/base/utils.mako" import="format_filelist" />
<div class='row'>
    <div class='col-md-4 col-xs-12'>
        % if is_invoice_list:
        ${request.layout_manager.render_panel('list_legend', legends=legends)}
        % endif
    </div>
</div>
<% num_columns = len(columns) + 1 %>
<table class="table table-condensed table-bordered status-table">
    <thead>
    % for column in columns:
        <th>
            % if column.sortable:
            ${sortable(column.label, column.sort_key)}
            % else:
            ${column.label | n}
            % endif
        </th>
    % endfor
        <th>Actions</th>
    </thead>
    <tbody>
        <tr>
            <td colspan='${num_columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## invoices are : Invoices, ManualInvoices or CancelInvoices
        % if records:
            % for document in records:
                <% id_ = document.id %>
                <% internal_number = document.internal_number %>
                <% name = document.name %>
                <% ht = document.ht %>
                <% tva = document.tva %>
                <% ttc = document.ttc %>
                <% status = document.status %>
                <% paid_status = getattr(document, 'paid_status', 'resulted') %>
                <% date = document.date %>
                <% type_ = document.type_ %>
                <% official_number = document.official_number %>
                % if is_admin_view:
                    <% company = document.get_company() %>
                    <% company_id = company.id %>
                    <% company_name = company.name %>
                % endif
                <% customer_id = document.customer.id %>
                <% customer_label = document.customer.label %>

                <tr class='status tolate-${document.is_tolate()} paid-status-${paid_status} status-${document.status}'>
                    <td
                        class='status-td'
                        title="${api.format_status(document)}"
                        >
                        <br />
                        </td>
            <td title="${api.format_status(document)}">
                ${official_number}
            </td>
            % if is_admin_view:
                <td>
                    ${company_name}
                </td>
            % endif
            <td>
                ${api.format_date(date)}
            </td>
            <td>
                <a href="${request.route_path('/%ss/{id}.html' % type_, id=id_)}"
                    title='Voir le document'>
                    ${internal_number} <br />(<small>${name}</small>)
                </a>
                % if not is_admin_view:
                    <% description = document.description %>
                    <small>
                        ${format_text(description)}
                    </small>
                % endif
            </td>
            <td class='invoice_company_name'>
                ${customer_label}
            </td>
            <td>
                <strong>${api.format_amount(ht, precision=5)|n}&nbsp;€</strong>
            </td>
            <td>
                ${api.format_amount(tva, precision=5)|n}&nbsp;€
            </td>
            <td>
                ${api.format_amount(ttc, precision=5)|n}&nbsp;€
            </td>
            <td>
                % if len(document.payments) == 1 and paid_status == 'resulted':
                    <% payment = document.payments[0] %>
                    <% url = request.route_path('payment', id=payment.id) %>
                    <a href="#!" onclick="window.openPopup('${url}')">
                    Le ${api.format_date(payment.date)}
                    (${api.format_paymentmode(payment.mode)})
                    </a>
                % elif len(document.payments) > 0:
                    <ul>
                        % for payment in document.payments:
                    <% url = request.route_path('payment', id=payment.id) %>
                            <li>
                                <a href="#!" onclick="window.openPopup('${url}')">
                                    ${api.format_amount(payment.amount, precision=5)|n}&nbsp;€
                                    le ${api.format_date(payment.date)}
                                    (${api.format_paymentmode(payment.mode)})
                                </a>
                            </li>
                        % endfor
                    </ul>
                % endif
            </td>
            <td>
                ${format_filelist(document)}
                % if hasattr(document, 'estimation_id') and document.estimation_id is not None:
                ${format_filelist(document.estimation)}
                % elif hasattr(document, 'invoice_id') and document.invoice_id is not None:
                ${format_filelist(document.invoice)}
                % endif
            </td>
            <td class='text-right'>
                ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(document))}
            </td>
        </tr>
        % endfor
    % else:
        <tr>
            <td colspan='${num_columns}'>
                <em>Aucune facture n'a pu être retrouvée</em>
            </td>
        </tr>
    % endif
    </tbody>
    <tfoot>
        <tr>
            <td colspan='${num_columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
    </tfoot>
</table>
