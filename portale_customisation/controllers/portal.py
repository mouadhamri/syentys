# -*- coding: utf-8 -*-

from collections import OrderedDict
from operator import itemgetter
from odoo import conf, http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR


class ProjectCustomerPortal(CustomerPortal):

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                        search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = self._task_get_searchbar_sortings()
        searchbar_sortings = dict(sorted(self._task_get_searchbar_sortings().items(),
                                         key=lambda item: item[1]["sequence"]))

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_inputs = self._task_get_searchbar_inputs()
        searchbar_groupby = self._task_get_searchbar_groupby()

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].search([])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', 'not in', projects.ids)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        # default group by value
        if not groupby:
            groupby = 'project'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        if request.session.uid and request.env['res.users'].browse(request.session.uid):
            res_user = request.env['res.users'].browse(request.session.uid)
            if res_user.partner_id:
                domain += [('project_id.partner_id','parent_of',res_user.partner_id.id)]

        # search
        if search and search_in:
            domain += self._task_get_search_domain(search_in, search)

        # task count
        task_count = request.env['project.task'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'groupby': groupby, 'search_in': search_in, 'search': search},
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        order = self._task_get_order(order, groupby)

        tasks = request.env['project.task'].sudo().search(domain, order=order, limit=self._items_per_page,
                                                          offset=pager['offset'])

        request.session['my_tasks_history'] = tasks.ids[:100]

        groupby_mapping = self._task_get_groupby_mapping()
        group = groupby_mapping.get(groupby)
        if group:
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in groupbyelem(tasks, itemgetter(group))]
        else:
            grouped_tasks = [tasks]

        task_states = dict(request.env['project.task']._fields['kanban_state']._description_selection(request.env))
        if sortby == 'status':
            if groupby == 'none' and grouped_tasks:
                grouped_tasks[0] = grouped_tasks[0].sorted(lambda tasks: task_states.get(tasks.kanban_state))
            else:
                grouped_tasks.sort(key=lambda tasks: task_states.get(tasks[0].kanban_state))

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'task',
            'default_url': '/my/tasks',
            'task_url': 'task',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("project.portal_my_tasks", values)

    def _task_get_search_domain(self, search_in, search):
        res = super(ProjectCustomerPortal, self)._task_get_search_domain(search_in=search_in, search=search)
        search_domain = []
        if search_in in ('content', 'all'):
            search_domain.append([('name', 'ilike', search)])
            search_domain.append([('description', 'ilike', search)])
            search_domain.append([('code', 'ilike', search)])
            return OR(search_domain)
        return res
