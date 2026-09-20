frappe.ui.form.on('Manifesto Eletronico Documentos', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            if (frm.doc.status === 'Autorizado') {
                frm.add_custom_button(__('Imprimir DAMDFE (PDF)'), function() {
                    window.open('/api/method/erpz_transporte.erpz_transporte.doctype.manifesto_eletronico_documentos.manifesto_eletronico_documentos.baixar_damdfe_pdf?docname=' + encodeURIComponent(frm.doc.name));
                }).addClass('btn-primary');

                frm.add_custom_button(__('Encerrar Viagem na SEFAZ'), function() {
                    frappe.confirm(__('Confirma o encerramento da viagem deste MDF-e na SEFAZ?'), function() {
                        frappe.dom.freeze(__('Enviando evento de encerramento de viagem para a SEFAZ...'));
                        frm.call({
                            method: 'encerrar_viagem_sefaz',
                            doc: frm.doc,
                            callback: function(r) {
                                frappe.dom.unfreeze();
                                frm.reload_doc();
                                if (r.message && r.message.success) {
                                    frappe.show_alert({ message: __('MDF-e Encerrado com Sucesso!'), indicator: 'green' });
                                }
                            }
                        });
                    });
                }, __('Eventos'));
            }

            if (frm.doc.status !== 'Autorizado' && frm.doc.status !== 'Encerrado') {
                frm.add_custom_button(__('Transmitir MDF-e para SEFAZ'), function() {
                    frappe.dom.freeze(__('Transmitindo MDF-e para a SEFAZ...'));
                    frm.call({
                        method: 'transmitir_sefaz',
                        doc: frm.doc,
                        callback: function(r) {
                            frappe.dom.unfreeze();
                            frm.reload_doc();
                            if (r.message && r.message.success) {
                                frappe.show_alert({
                                    message: __('MDF-e Autorizado com Sucesso! Nº ' + r.message.numero_mdfe),
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
