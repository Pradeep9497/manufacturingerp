from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
from datetime import date
import openerp.addons.decimal_precision as dp
from datetime import datetime
dt_time = time.strftime('%m/%d/%Y %H:%M:%S')

class kite_gate_pass(osv.osv):

	_name = "kite.gate.pass"
	_description = "kite Service"
	_order = "creation_date desc"
	
	_columns = {
		'name': fields.char('Service Indent No',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'ind_date': fields.datetime('Service Indent Date',size=128),
		'dept_name': fields.many2one('kite.department.master','Department Name',readonly=True,states={'draft': [('readonly', False)]}),
		'dept_code': fields.char('Department Code',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'service': fields.char('Service Machinery',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'creation_date':fields.datetime('Creation Date',readonly=True),
		'state': fields.selection([('draft', 'Draft'),('cancel', 'Cancelled'),('confirm', 'Confirmed')],'Status'),
		'active':fields.boolean('Active'),
		
		##############
		'line_id':fields.one2many('kite.gate.pass.line','product_id','product_line',readonly=True,states={'draft': [('readonly', False)]}),

	}
	_defaults = {
		'creation_date': fields.date.context_today,
		'state':'draft',
		'active':True,
		
	   }
  
	   
	def create(self, cr, uid, vals,context=None):		
		if vals.get('name','/')=='/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'kite.gate.pass') or '/'
		order =  super(kite_gate_pass, self).create(cr, uid, vals, context=context)
		return order
	def confirm_purchase(self,cr,uid,ids,context=None):
		purchase_plan_obj = self.pool.get('kite.gate.pass')
		rec = self.browse(cr,uid,ids[0])
		rec.write({'state':'confirm'})
	
	
kite_gate_pass()

class kite_gate_pass_line(osv.osv):
	
	_name = "kite.gate.pass.line"
	_description = "Kite gate pass line"
	
	_columns = {
		
		
		'product_name':fields.many2one('product.product','Product Name'),
		'product_code':fields.char('Product Code',size=128),
		'unit_price':fields.float('Unit Price'),
		'required_qty':fields.float('Required Qty'),
		'product_id':fields.many2one('kite.service.indent','Product line'),
		'pro_type':fields.selection([('direct','Direct'),('fromcp','From purchase Plan')],'Production Type'),
	}
	
	_defaults = {
		'pro_type' : 'direct',
		}
		
	
	
		
kite_gate_pass_line()


