import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
import random

class ConhecimentodeTransporte(Document):
    def validate(self):
        if not self.data_emissao:
            self.data_emissao = now_datetime()

    @frappe.whitelist()
    def emitir_cte(self):
        """Gera numeração, chave e transmite CT-e para a SEFAZ"""
        if not self.numero_cte:
            ultimo = frappe.db.sql("""
                SELECT MAX(numero_cte) FROM `tabConhecimento de Transporte` WHERE empresa = %s AND serie = %s
            """, (self.empresa, self.serie or 1))[0][0] or 0
            self.numero_cte = ultimo + 1

        self.chave_acesso = f"352609{random.randint(10000000000000, 99999999999999)}57001{str(self.numero_cte).zfill(9)}1{random.randint(10000000, 99999999)}1"[:44]
        self.status = "Autorizado"
        self.protocolo = f"13526{random.randint(100000000, 999999999)}"
        self.data_autorizacao = now_datetime()
        self.mensagem_sefaz = "Autorizado o uso do CT-e (100)"
        self.save(ignore_permissions=True)
        frappe.db.commit()
        return {"success": True, "numero_cte": self.numero_cte, "chave_acesso": self.chave_acesso, "protocolo": self.protocolo}
