app_name = "erpz_transporte"
app_title = "ERPZ Transporte"
app_publisher = "ERPZ"
app_description = "Gestão de Transporte, Expedição, Montagem de Cargas, Cubagem, CT-e e MDF-e"
app_email = "dev@erpz.io"
app_license = "mit"
app_version = "0.0.1"

required_apps = ["frappe", "erpnext", "erpz_fiscal"]

after_install = "erpz_transporte.setup.after_install"
after_migrate = "erpz_transporte.setup.after_migrate"

doc_events = {
    "Sales Order": {
        "validate": "erpz_transporte.api.calcular_pesos_sales_order"
    }
}
