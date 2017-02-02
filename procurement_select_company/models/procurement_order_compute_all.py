# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from openerp.api import Environment

import logging
import threading
from openerp import SUPERUSER_ID
from openerp import tools


class ProcurementOrderComputeAll(models.TransientModel):

    _inherit = 'procurement.order.compute.all'

    company_ids = fields.Many2many(
        'res.company',
        default=lambda self: self.env.user.company_ids,
	)

    def _procure_calculation_all(self, cr, uid, ids, context=None):
        """
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        """
        import ipdb; ipdb.set_trace() # BREAKPOINT
        with Environment.manage():
            proc_obj = self.pool.get('procurement.order')
            #As this function is in a new thread, i need to open a new cursor, because the old one may be closed

            new_cr = self.pool.cursor()
            scheduler_cron_id = self.pool['ir.model.data'].get_object_reference(new_cr, SUPERUSER_ID, 'procurement', 'ir_cron_scheduler_action')[1]
            # Avoid to run the scheduler multiple times in the same time
            try:
                with tools.mute_logger('openerp.sql_db'):
                    new_cr.execute("SELECT id FROM ir_cron WHERE id = %s FOR UPDATE NOWAIT", (scheduler_cron_id,))
            except Exception:
                _logger.info('Attempt to run procurement scheduler aborted, as already running')
                new_cr.rollback()
                new_cr.close()
                return {}
#            user = self.pool.get('res.users').browse(new_cr, uid, uid, context=context)
#            comps = [x.id for x in user.company_ids]
#            for comp in comps:
#                proc_obj.run_scheduler(new_cr, uid, use_new_cursor=new_cr.dbname, company_id = comp, context=context)

            import ipdb; ipdb.set_trace() # BREAKPOINT
            comps = self.browse(new_cr, uid, ids, context=context).company_ids
            for comp in comps:
                proc_obj.run_scheduler(new_cr, uid, use_new_cursor=new_cr.dbname, company_id = comp.id, context=context)
            #close the new cursor
            new_cr.close()
            return {}

#    def _procure_calculation_all(self, cr, uid, ids, context=None):
#        import ipdb; ipdb.set_trace() # BREAKPOINT
#        with Environment.manage():
#            # As this function is in a new thread, i need to open a new cursor, because the old one may be closed
#            new_cr = registry(self._cr.dbname).cursor()
#            self = self.with_env(self.env(cr=new_cr))  # TDE FIXME
#            scheduler_cron = self.sudo().env.ref('procurement.ir_cron_scheduler_action')
#            # Avoid to run the scheduler multiple times in the same time
#            try:
#                with tools.mute_logger('odoo.sql_db'):
#                    self._cr.execute("SELECT id FROM ir_cron WHERE id = %s FOR UPDATE NOWAIT", (scheduler_cron.id,))
#            except Exception:
#                _logger.info('Attempt to run procurement scheduler aborted, as already running')
#                self._cr.rollback()
#                self._cr.close()
#                return {}
#
#            Procurement = self.env['procurement.order']
#            for company in self.company_ids:
#                Procurement.run_scheduler(use_new_cursor=self._cr.dbname, company_id=company.id)
#            # close the new cursor
#            self._cr.close()
#        return {}
