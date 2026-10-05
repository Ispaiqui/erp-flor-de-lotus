# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Ganchos da camada Flor de Lótus.

Nada aqui altera arquivos do ERPNext. Título, logo e tema entram pelos
ganchos e, na instalação, pelos Single DocTypes de configuração do site
(System Settings, Website Settings, Navbar Settings).
"""

from flor_de_lotus.brand import APP_TITLE, FAVICON_URL, LOGO_URL, MARK_URL, PALETTE, SPLASH_URL

app_name = "flor_de_lotus"
app_title = APP_TITLE
app_publisher = "Flor de Lótus"
app_description = "Camada de produto da Flor de Lótus sobre o ERPNext: marca e vocabulário da operação."
app_color = PALETTE["primary"]
app_license = "GNU General Public License (v3)"
app_logo_url = LOGO_URL
source_link = "https://github.com/Ispaiqui/erp-flor-de-lotus"

required_apps = ["erpnext"]

add_to_apps_screen = [
	{
		"name": app_name,
		"logo": MARK_URL,
		"title": app_title,
		"route": "/desk",
		"setup_wizard_text": "Marca e nomes da operação Flor de Lótus.",
		"has_permission": "flor_de_lotus.permissions.check_app_permission",
		"sequence_id": 2,
	}
]

app_include_css = ["/assets/flor_de_lotus/css/flor_de_lotus.css"]
web_include_css = ["/assets/flor_de_lotus/css/flor_de_lotus.css"]

website_context = {
	"favicon": FAVICON_URL,
	"splash_image": SPLASH_URL,
	"app_name": APP_TITLE,
}

update_website_context = "flor_de_lotus.boot.update_website_context"
extend_bootinfo = "flor_de_lotus.boot.extend_bootinfo"
boot_session = "flor_de_lotus.boot.extend_bootinfo"

after_install = "flor_de_lotus.install.after_install"
after_migrate = "flor_de_lotus.install.after_migrate"
