import frappe
import json, os

def setup_desktop_and_sidebar():
    icon_name = frappe.db.get_value("Desktop Icon", {"link_to": "ERPZ Transporte"}, "name")
    if not icon_name:
        icon_name = frappe.db.get_value("Desktop Icon", {"label": "ERPZ Transporte"}, "name")

    icon_data = {
        "label": "ERPZ Transporte",
        "icon": "truck",
        "icon_type": "Link",
        "link_type": "Workspace Sidebar",
        "link_to": "ERPZ Transporte",
        "parent_icon": "",
        "hidden": 0,
        "standard": 1,
        "app": "erpz_transporte",
        "idx": 9
    }

    if icon_name:
        frappe.db.set_value("Desktop Icon", icon_name, icon_data)
    else:
        new_icon = frappe.new_doc("Desktop Icon")
        new_icon.name = "ERPZ Transporte"
        new_icon.update(icon_data)
        new_icon.insert(ignore_permissions=True)

    # Sync Workspace Sidebar
    sb_file = "/home/frappe/frappe-bench/apps/erpz_transporte/erpz_transporte/workspace_sidebar/erpz_transporte.json"
    if os.path.exists(sb_file):
        with open(sb_file, "r", encoding="utf-8") as fp:
            sb_data = json.load(fp)

        if frappe.db.exists("Workspace Sidebar", "ERPZ Transporte"):
            sb = frappe.get_doc("Workspace Sidebar", "ERPZ Transporte")
            sb.items = []
            for it in sb_data.get("items", []):
                sb.append("items", it)
            sb.save(ignore_permissions=True)
        else:
            sb = frappe.new_doc("Workspace Sidebar")
            sb.update(sb_data)
            sb.insert(ignore_permissions=True)


def create_custom_fields():
    fields = {
        "Sales Order": [
            {
                "fieldname": "erpz_transporte_section",
                "label": "Volumes e Pesos da Carga",
                "fieldtype": "Section Break",
                "insert_after": "terms",
                "collapsible": 1
            },
            {
                "fieldname": "volumes",
                "label": "Volumes",
                "fieldtype": "Float",
                "default": "1",
                "insert_after": "erpz_transporte_section"
            },
            {
                "fieldname": "column_break_transp_so",
                "fieldtype": "Column Break",
                "insert_after": "volumes"
            },
            {
                "fieldname": "peso_liquido",
                "label": "Peso Líquido Total (kg)",
                "fieldtype": "Float",
                "precision": "3",
                "insert_after": "column_break_transp_so"
            },
            {
                "fieldname": "peso_bruto",
                "label": "Peso Bruto Total (kg)",
                "fieldtype": "Float",
                "precision": "3",
                "insert_after": "peso_liquido"
            }
        ]
    }
    for doctype, field_list in fields.items():
        for f in field_list:
            fname = f"{doctype}-{f['fieldname']}"
            if not frappe.db.exists("Custom Field", fname):
                cf = frappe.new_doc("Custom Field")
                cf.dt = doctype
                cf.module = "ERPZ Transporte"
                cf.update(f)
                cf.insert(ignore_permissions=True)
            else:
                frappe.db.set_value("Custom Field", fname, "module", "ERPZ Transporte")

def after_install():
    create_custom_fields()
    setup_desktop_and_sidebar()
    frappe.db.commit()

def after_migrate():
    create_custom_fields()
    setup_desktop_and_sidebar()
    frappe.db.commit()
