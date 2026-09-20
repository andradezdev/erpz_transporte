frappe.ui.form.on('Conhecimento de Transporte', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            if (frm.doc.status === 'Autorizado') {
                frm.add_custom_button(__('Imprimir DACTE (PDF)'), function() {
                    window.open('/api/method/erpz_transporte.erpz_transporte.doctype.conhecimento_de_transporte.conhecimento_de_transporte.baixar_dacte_pdf?docname=' + encodeURIComponent(frm.doc.name));
                }).addClass('btn-primary');
            }

            if (frm.doc.status !== 'Autorizado') {
                frm.add_custom_button(__('Transmitir CT-e para SEFAZ'), function() {
                    frappe.dom.freeze(__('Transmitindo CT-e para a SEFAZ...'));
                    frm.call({
                        method: 'transmitir_sefaz',
                        doc: frm.doc,
                        callback: function(r) {
                            frappe.dom.unfreeze();
                            frm.reload_doc();
                            if (r.message && r.message.success) {
                                frappe.show_alert({
                                    message: __('CT-e Autorizado com Sucesso! Nº ' + r.message.numero_cte),
                                    indicator: 'green'
                                });
                            }
                        }
                    });
                }).addClass('btn-primary');
            }
        }
    }
});
