from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
from datetime import date
import openerp.addons.decimal_precision as dp
from datetime import datetime
dt_time = time.strftime('%m/%d/%Y %H:%M:%S')

class kite_service_indent(osv.osv):

	_name = "kite.service.indent"
	_description = "kite Service"
	_order = "creation_date desc"
	
	_columns = {
		'name': fields.char('Service Indent No',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'ind_date': fields.datetime('Service Indent Date',size=128),
		'dept_name': fields.many2one('kite.department.master','Department Name',readonly=True,states={'draft': [('readonly', False)]}),
		'dept_code': fields.char('Department Code',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'creation_date':fields.datetime('Creation Date',readonly=True),
		'state': fields.selection([('draft', 'Draft'),('cancel', 'Cancelled'),('confirm', 'Confirmed')],'Status'),
		'active':fields.boolean('Active'),
		
		##############
		'line_id':fields.one2many('kite.service.indent.line','product_id','product_line',readonly=True,states={'draft': [('readonly', False)]}),

	}
	_defaults = {
		'creation_date': fields.date.context_today,
		'state':'draft',
		'active':True,
		
	   }
	def onchange_product(self, cr, uid, ids,dept_name,dept_code,context=None):
		dcode =""
		value = {'dept_code':''}
		partner_obj = self.pool.get('kite.department.master')
		result = partner_obj.browse(cr, uid, dept_name)
		if result:
			dcode = result.dept_code
			value={'dept_code':dcode}
			return {'value': value}   
	   
	def create(self, cr, uid, vals,context=None):		
		if vals.get('name','/')=='/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'kite.service.indent') or '/'
		order =  super(kite_service_indent, self).create(cr, uid, vals, context=context)
		return order
	def confirm_purchase(self,cr,uid,ids,context=None):
		purchase_plan_obj = self.pool.get('kite.service.indent')
		rec = self.browse(cr,uid,ids[0])
		rec.write({'state':'confirm'})
	
	
	
kite_service_indent()

class kite_service_indent_line(osv.osv):
	
	_name = "kite.service.indent.line"
	_description = "Kite Service Indent line"
	
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
		
	def onchange_product(self, cr, uid, ids,name,unit_price,product_code,context=None):
		price = ""
		code =""
		value = {'unit_price':'','product_code':''}
		partner_obj = self.pool.get('product.product')
		result = partner_obj.browse(cr, uid, name)
		if result:
			price = result.list_price 
			code = result.pro_code
			value={'unit_price':price,'product_code':code}
			return {'value': value} 
	
		
kite_service_indent_line()


