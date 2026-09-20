import frappe
from frappe.utils import flt

def calcular_pesos_sales_order(doc, method=None):
    """Calcula automaticamente os pesos bruto e líquido do Pedido de Venda a partir dos itens"""
    if not doc.items:
        return

    tot_pl = 0.0
    tot_pb = 0.0

    for item in doc.items:
        pl = flt(frappe.db.get_value("Item", item.item_code, "peso_liquido") or 0)
        pb = flt(frappe.db.get_value("Item", item.item_code, "peso_bruto") or 0)
        tot_pl += flt(item.qty) * pl
        tot_pb += flt(item.qty) * pb

    doc.peso_liquido = tot_pl
    doc.peso_bruto = tot_pb
    if not flt(doc.volumes):
        doc.volumes = 1.0
