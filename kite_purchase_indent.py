from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
import openerp.addons.decimal_precision as dp

class kite_purchase_indent(osv.osv):

	_name = "kite.purchase.indent"
	_description = "kite Purchase Indent"
	_order = "creation_date desc"
	
	_columns = {
		'ind_no': fields.char('Department Indent No',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'ind_date': fields.char('Department Indent Date',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'dept_name': fields.char('Department Name',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'dept_code': fields.char('Department code',size=128, select=True,readonly=True,states={'draft': [('readonly', False)]}),
		'name': fields.char('Purchase Indent No',size=128,readonly=True,states={'draft': [('readonly', False)]}),
		'creation_date':fields.date('Creation Date',readonly=True),
		'state': fields.selection([('draft', 'Draft'),('cancel', 'Cancelled'),('confirm', 'Confirmed')],'Status'),
		'active':fields.boolean('Active'),
		
		##################
		'line_id':fields.one2many('kite.purchase.indent.line','product_id','product_line',readonly=True,states={'draft': [('readonly', False)]}),

	}
	_defaults = {
		'creation_date': fields.date.context_today,
		'state':'draft',
		'active':True,
		
	   }
	
	   
	def create(self, cr, uid, vals,context=None):		
		if vals.get('name','/')=='/':
			vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'kite.purchase.indent') or '/'
		order =  super(kite_purchase_indent, self).create(cr, uid, vals, context=context)
		return order
	def confirm_purchase(self,cr,uid,ids,context=None):
		purchase_plan_obj = self.pool.get('kite.purchase.indent')
		rec = self.browse(cr,uid,ids[0])
		rec.write({'state':'confirm'})
		
	def approve(self,cr,uid,ids,context=None):
		kite_pur = self.pool.get('kite.purchase')
		rec = self.browse(cr,uid,ids[0])
		m_qa_vals = {
		'state':'draft',
		'name':rec.name,
		'ind_no':rec.ind_no,
		'ind_date':rec.ind_date,
		'dept_name':rec.dept_name,
		'dept_code':rec.dept_code,
		}
		m_qa_form_id = kite_pur.create(cr,uid,m_qa_vals,context=None)			
		for ele in rec.line_id:
			m_qa_val = {
			'product_name':ele.product_name,
			'product_code':ele.product_code,
			'product_id':m_qa_form_id,
			'unit_price':ele.unit_price,
			'required_qty':ele.required_qty,
			}
			qa_form_id = self.pool.get('kite.purchase.line').create(cr,uid,m_qa_val,context=None)
	
	
kite_purchase_indent()

class kite_purchase_indent_line(osv.osv):
	
	_name = "kite.purchase.indent.line"
	_description = "Kite Purchase Indent line"
	
	_columns = {
		
		'product_name':fields.char('Product Name'),
		'product_code':fields.char('Product Code',size=128),
		'unit_price':fields.float('Unit Price'),
		'required_qty':fields.float('Required Qty'),
		'product_id':fields.many2one('kite.purchase.indent','Product line'),
		'pro_type':fields.selection([('direct','Direct'),('fromcp','From purchase Plan')],'Production Type'),
	}
	
	_defaults = {
		'pro_type' : 'direct',
		}
		
	
			
	
		
kite_purchase_indent_line()


