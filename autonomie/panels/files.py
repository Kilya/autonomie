# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.widgets import Link
from autonomie.models.node import Node


def stream_actions(request, item):
    """
    Collect actions available for the given item
    """
    if request.has_permission('edit.file', item):
        yield Link(
            request.route_path('file', id=item.id),
            u"Voir le détail / Modifier",
            icon='pencil',
        )
    if request.has_permission('view.file', item):
        yield Link(
            request.route_path(
                'file', id=item.id, _query=dict(action='download')
            ),
            u"Télécharger",
            icon="download",
        )

    if request.context.id == item.parent_id:
        if request.has_permission('delete.file', item):
            yield Link(
                request.route_path(
                    'file', id=item.id, _query=dict(action='delete')
                ),
                u"Supprimer",
                confirm=u"Êtes-vous sûr de vouloir définitivement supprimer "
                u"ce fichier ?",
                icon="trash",
            )


def parent_label(node):
    """
    Render a label for the given node

    :param obj node: :class:`autonomie.models.node.Node` instance
    :returns: A label for filetable display
    """
    return u"{0} : {1}".format(
        Node.NODE_LABELS.get(node.parent.type_, u"Donnée"),
        node.parent.name,
    )


def filetable_panel(
    context, request, add_url, files, add_perm="add.file", help_message=None,
    show_parent=False,
):
    """
    render a table listing files

    files should be loaded with the following columns included :

        description
        updated_at
        id
        parent.id
        parent.name
        parent.type_


    :param obj context: The context for which we display the files
    :param str add_url: The url for adding elements
    :param list files: A list of :class:`autonomie.models.files.File`
    :param str add_perm: The permission required to add a file
    :param str help_message: An optionnal help message
    :param bool show_parent: Should a column show the parent ?
    :returns: dict
    """
    return dict(
        files=files,
        add_url=add_url,
        stream_actions=stream_actions,
        add_perm=add_perm,
        help_message=help_message,
        parent_label=parent_label,
        show_parent=show_parent,
    )


def includeme(config):
    config.add_panel(
        filetable_panel,
        'filetable',
        renderer='panels/filetable.mako',
    )
