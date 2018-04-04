from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
from datetime import date
import openerp.addons.decimal_precision as dp
from datetime import datetime
dt_time = time.strftime('%m/%d/%Y %H:%M:%S')


class kite_purchase(osv.osv):

	_name = "kite.purchase"
	_description = "KG Purchase"
	_order = "creation_date desc"
	
	def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		for order in self.browse(cr, uid, ids, context=context):
			res[order.id] = {
				'amount_total': 0.0,
			}
			val1 =0
			for line in order.line_id:
				val1 += line.required_qty * line.unit_price 
			res[order.id]['amount_total']=(round(val1))
		return res
		
	_columns = {
		'name': fields.char('Purchase Indent No',size=128,readonly=True,states={'draft': [('readonly', False)]}),
		'supplier':fields.many2one('res.partner','Supplier',size=128),
		'ind_no': fields.char('Department Indent No',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'ind_date': fields.char('Department Indent Date',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'dept_name': fields.char('Department Name',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'dept_code': fields.char('Department code',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'creation_date':fields.datetime('Creation Date',readonly=True),
		'state': fields.selection([('draft', 'Draft'),('cancel', 'Cancelled'),('confirm', 'Confirmed')],'Status'),
		'active':fields.boolean('Active'),
		'amount_total': fields.function(_amount_all, string='Total',store=True,multi="sums",help="The total amount"),

	#################
		'line_id':fields.one2many('kite.purchase.line','product_id','product_line',readonly=True,states={'draft': [('readonly', False)]}),

		
	}
	_defaults = {
		'creation_date': fields.date.context_today,
		'state':'draft',
		'active':True,
		'creation_date' : lambda * a: time.strftime('%Y-%m-%d'),

	   }
	
	    
	   
	def create(self, cr, uid, vals,context=None):		
		if vals.get('name','/')=='/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'kite.purchase') or '/'
		order =  super(kite_purchase, self).create(cr, uid, vals, context=context)
		return order
	
	def confirm(self,cr,uid,ids,context=None):
		purchase_plan_obj = self.pool.get('kite.purchase.planning')
		rec = self.browse(cr,uid,ids[0])
		rec.write({'state':'confirm'})
		
		ir_mail_server = self.pool.get('ir.mail_server')
		msg = ir_mail_server.build_email(
			  email_from = ['radeepp0@gmail.com'],
			  email_to = ['prasanthnsn11@gmail.com'],
			  subject = 'Test',
			  body = 'Hi Nice',
			  #~ email_cc = 'prasanth@gmail.com',
			  object_id = ids and ('%s-%s' % (ids, 'purchase.indent')),
			  subtype = 'html',
			  subtype_alternative = 'plain')
		res = ir_mail_server.send_email(cr, uid, msg,mail_server_id=2,  context=context)
		print"successs.............................................."
		return True

kite_purchase()

class kite_purchase_line(osv.osv):
	
	_name = "kite.purchase.line"
	_description = "KG Purchase line"
	
	_columns = {
		
		
		'product_name':fields.char('Product Name'),
		'product_code':fields.char('Product Code',size=128),
		'unit_price':fields.float('Unit Price'),
		'required_qty':fields.float('Required Qty'),
		'total_price':fields.float('Total price'),
		'product_id':fields.many2one('kite.purchase','Product line'),
		'pro_type':fields.selection([('direct','Direct'),('fromcp','From purchase Plan')],'Production Type'),
	}
	
	_defaults = {
		'pro_type' : 'direct',
		}
		

			
	
		
kite_purchase_line()
