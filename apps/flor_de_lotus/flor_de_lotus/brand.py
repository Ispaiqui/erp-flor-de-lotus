# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Marca provisória da Flor de Lótus.

As cores ainda não foram decididas. A paleta abaixo é um placeholder
calmo (rosa de lótus e verde profundo) para o tema existir num lugar só.

Para mudar as cores, edite ``PALETTE`` e regenere o CSS:

    python -m flor_de_lotus.build_assets

O logo provisório está em ``public/images/``. Substitua os arquivos SVG.
``python -m flor_de_lotus.build_assets --with-logos`` repinta esses SVG
com a paleta atual e apaga um logo que você tenha colocado no lugar.
"""

from __future__ import annotations

APP_NAME = "flor_de_lotus"
APP_TITLE = "Flor de Lótus"

# Placeholder. Não é a paleta oficial da loja.
PALETTE: dict[str, str] = {
	"primary": "#C46B84",
	"primary_strong": "#9A4E66",
	"secondary": "#1E4D3A",
	"secondary_soft": "#E5F0EA",
	"surface": "#FBF8F6",
	"ink": "#1C2421",
	"muted": "#5C6560",
	"line": "#E7DED8",
	"on_primary": "#FFFFFF",
}

LOGO_URL = "/assets/flor_de_lotus/images/flor-de-lotus-logo-placeholder.svg"
MARK_URL = "/assets/flor_de_lotus/images/flor-de-lotus-mark-placeholder.svg"
FAVICON_URL = MARK_URL
SPLASH_URL = LOGO_URL

# Valores que o Frappe e o ERPNext deixam antes de qualquer marca da loja.
# A instalação só troca o que ainda estiver nesta lista.
DEFAULT_APP_NAMES = frozenset({None, "", "Frappe", "ERPNext"})
DEFAULT_LOGO_URLS = frozenset(
	{
		None,
		"",
		"/assets/frappe/images/frappe-framework-logo.svg",
		"/assets/frappe/images/frappe-favicon.svg",
		"/assets/erpnext/images/erpnext-logo.svg",
		"/assets/erpnext/images/erpnext-favicon.svg",
		"/assets/erpnext/images/erpnext-logo.png",
	}
)
DEFAULT_FAVICON_URLS = frozenset(
	{
		None,
		"",
		"/assets/frappe/images/frappe-favicon.svg",
		"/assets/erpnext/images/erpnext-favicon.svg",
		"/assets/frappe/images/favicon.png",
	}
)

BRAND_HTML = (
	f'<img src="{LOGO_URL}" alt="{APP_TITLE}" '
	'style="max-height:72px;width:auto" data-placeholder="flor-de-lotus">'
)


def render_theme_css() -> str:
	"""CSS do desk e do site. As cores vêm só de ``PALETTE``."""
	color = PALETTE
	return f"""/* Tema provisório da Flor de Lótus.
   As cores NÃO estão decididas. Edite flor_de_lotus/brand.py (PALETTE)
   e rode: python -m flor_de_lotus.build_assets
   Não espalhe estes hex por outros arquivos. */

:root {{
	--fdl-color-primary: {color["primary"]};
	--fdl-color-primary-strong: {color["primary_strong"]};
	--fdl-color-secondary: {color["secondary"]};
	--fdl-color-secondary-soft: {color["secondary_soft"]};
	--fdl-color-surface: {color["surface"]};
	--fdl-color-ink: {color["ink"]};
	--fdl-color-muted: {color["muted"]};
	--fdl-color-line: {color["line"]};
	--fdl-color-on-primary: {color["on_primary"]};

	/* Ponte com as variáveis que o Desk ainda consulta. */
	--primary: var(--fdl-color-primary);
	--primary-color: var(--fdl-color-primary);
}}

.btn-primary,
.btn-primary:focus,
.btn-primary:active {{
	background-color: var(--fdl-color-primary);
	border-color: var(--fdl-color-primary-strong);
	color: var(--fdl-color-on-primary);
}}

.btn-primary:hover {{
	background-color: var(--fdl-color-primary-strong);
	border-color: var(--fdl-color-primary-strong);
	color: var(--fdl-color-on-primary);
}}

.navbar {{
	box-shadow: inset 0 -2px 0 var(--fdl-color-primary);
}}

.navbar-brand img,
.navbar .navbar-brand img {{
	max-height: 28px;
	width: auto;
}}

.page-card-head img,
.for-login .page-card-head img {{
	max-height: 72px;
	width: auto;
}}

body[data-path="login"],
.for-login {{
	background: var(--fdl-color-surface);
}}
"""


def _petals(primary: str) -> str:
	return f"""<g fill="{primary}" transform="translate(32 42)">
    <ellipse cx="0" cy="-14" rx="6" ry="13"/>
    <ellipse cx="0" cy="-13" rx="5.5" ry="12" transform="rotate(-38)"/>
    <ellipse cx="0" cy="-13" rx="5.5" ry="12" transform="rotate(38)"/>
    <ellipse cx="0" cy="-11" rx="5" ry="11" transform="rotate(-72)"/>
    <ellipse cx="0" cy="-11" rx="5" ry="11" transform="rotate(72)"/>
  </g>
  <circle cx="32" cy="42" r="4.2" fill="{PALETTE["surface"]}"/>"""


def render_mark_svg() -> str:
	primary = PALETTE["primary"]
	secondary = PALETTE["secondary"]
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- PLACEHOLDER: marca provisória da Flor de Lótus.
     Substitua este arquivo quando houver o logo definitivo.
     Cores copiadas de flor_de_lotus/brand.py (PALETTE). -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Flor de Lótus, marca provisória">
  <title>Flor de Lótus — marca provisória</title>
  <desc>PLACEHOLDER. Não é o logo oficial. Troque este SVG.</desc>
  <rect width="64" height="64" rx="16" fill="{secondary}"/>
  {_petals(primary)}
</svg>
"""


def render_logo_svg() -> str:
	primary = PALETTE["primary"]
	secondary = PALETTE["secondary"]
	surface = PALETTE["surface"]
	muted = PALETTE["muted"]
	ink = PALETTE["ink"]
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- PLACEHOLDER: logo provisório da Flor de Lótus, com o nome escrito para
     a tela de entrada. Substitua este arquivo quando houver o logo definitivo.
     Cores copiadas de flor_de_lotus/brand.py (PALETTE). -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 80" role="img" aria-label="Flor de Lótus, logo provisório">
  <title>Flor de Lótus — logo provisório</title>
  <desc>PLACEHOLDER. Não é o logo oficial. Troque este SVG.</desc>
  <rect width="420" height="80" rx="12" fill="{surface}"/>
  <g transform="translate(8 8)">
    <rect width="64" height="64" rx="16" fill="{secondary}"/>
    {_petals(primary)}
  </g>
  <text x="88" y="38" fill="{ink}" font-family="Georgia, 'Palatino Linotype', Palatino, serif" font-size="28">Flor de Lótus</text>
  <text x="88" y="58" fill="{muted}" font-family="Georgia, 'Palatino Linotype', Palatino, serif" font-size="12" letter-spacing="1.5">PLACEHOLDER · MARCA PROVISÓRIA</text>
</svg>
"""
