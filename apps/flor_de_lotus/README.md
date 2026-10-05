# Flor de Lótus

Camada de produto para a operação da Flor de Lótus: cinco lojas, um depósito central, PDV e fabricação de velas, em cima do ERPNext.

Esta versão só traz a **marca** e os **nomes em português**. Não há loja, caixa, catálogo de velas nem regra fiscal. Isso vem nas versões seguintes, dentro deste app, sem editar o núcleo do ERPNext.

Licença: GPL-3.0, a mesma do ERPNext. O texto está em `license.txt`.

## Por que o app fica em `apps/flor_de_lotus/`

A raiz deste repositório continua sendo o app **erpnext**. É isso que o `bench get-app` instala quando aponta para o fork. O pacote `erpnext/` e o `pyproject.toml` da raiz não foram alterados.

A camada da loja é um segundo app Frappe, completo, em `apps/flor_de_lotus/`:

- `pyproject.toml` e `license.txt` na pasta do app
- pacote Python `flor_de_lotus/` com `hooks.py`, `modules.txt` e `patches.txt`
- `required_apps = ["erpnext"]`

Assim o fork segue perto do upstream, e o que for da Flor de Lótus não se mistura com o código do ERPNext. A pasta não é um repositório git próprio: o git é o do fork. Por isso o `bench get-app --soft-link` (ele exige um `.git` dentro da pasta do app) não é o caminho usado abaixo.

## Instalar num bench

O bench precisa do Frappe 17 (o `develop` deste fork pede `frappe >= 17`) e do ERPNext **deste** repositório já instalado no site. Este ambiente de desenvolvimento não sobe um bench; os comandos são o que se roda na máquina do bench.

Na raiz do bench, com o fork já em `apps/erpnext`:

```bash
ln -s "$(pwd)/apps/erpnext/apps/flor_de_lotus" apps/flor_de_lotus
./env/bin/pip install -e apps/flor_de_lotus
grep -qx flor_de_lotus sites/apps.txt || echo flor_de_lotus >> sites/apps.txt
bench --site SEU_SITE install-app flor_de_lotus
bench build --app flor_de_lotus
bench --site SEU_SITE clear-cache
```

`install-app` grava o nome **Flor de Lótus**, o logo, o favicon e a imagem de abertura nos ajustes do site, se eles ainda estiverem com o padrão do Frappe ou do ERPNext. Se o idioma ainda for inglês, passa para `pt-BR`.

O usuário também precisa estar em português do Brasil para ver os nomes da lista. Em **System Settings**, idioma `pt-BR`. Saia e entre de novo, e atualize a página sem cache.

Para repor a marca provisória depois de um teste:

```bash
bench --site SEU_SITE execute flor_de_lotus.install.apply_branding --kwargs '{"overwrite": true}'
bench --site SEU_SITE clear-cache
```

`overwrite` troca também um logo que você já tenha colocado. Sem isso, uma migração não desfaz a sua escolha.

## Trocar o logo

Os arquivos atuais são placeholders. O nome deixa isso explícito, e o SVG contém a palavra `PLACEHOLDER`.

| Uso | Arquivo |
| --- | --- |
| Tela de entrada, barra e splash | `flor_de_lotus/public/images/flor-de-lotus-logo-placeholder.svg` |
| Ícone do app e favicon | `flor_de_lotus/public/images/flor-de-lotus-mark-placeholder.svg` |

Substitua o conteúdo (pode manter o nome do arquivo) ou aponte `LOGO_URL`, `MARK_URL`, `FAVICON_URL` e `SPLASH_URL` em `flor_de_lotus/brand.py` para os arquivos novos. Em seguida:

```bash
bench build --app flor_de_lotus
bench --site SEU_SITE clear-cache
```

Se o site já gravou o caminho antigo em **Website Settings** ou **Navbar Settings**, atualize o logo nessas telas ou rode o `execute` acima.

Não use `--with-logos` (abaixo) depois de colocar o logo definitivo: esse comando reescreve os SVG provisórios.

## Trocar as cores

As cores **não estão decididas**. A paleta é um placeholder: rosa de lótus (`#C46B84`) e verde profundo (`#1E4D3A`), num fundo de papel. O único lugar para mudá-las é o dicionário `PALETTE` em `flor_de_lotus/brand.py`.

Na pasta do app (ou com o pacote no `PYTHONPATH`):

```bash
python -m flor_de_lotus.build_assets
bench build --app flor_de_lotus
bench --site SEU_SITE clear-cache
```

Isso reescreve `flor_de_lotus/public/css/flor_de_lotus.css`. O tema usa variáveis `--fdl-color-*` e aponta `--primary` para a cor principal. Enquanto a marca provisória estiver em uso, para pintar os SVG com a paleta nova:

```bash
python -m flor_de_lotus.build_assets --with-logos
```

`app_color` no `hooks.py` também sai de `PALETTE`. Não copie o hex para outro arquivo.

## Nomes em português

A lista e o motivo de cada escolha estão em [GLOSSARIO.md](GLOSSARIO.md). Resumo do que a equipe vê:

| Na loja | No ERPNext |
| --- | --- |
| Produto | Item |
| Depósito | Warehouse |
| Estoque | Stock (a quantidade, não o lugar) |
| PDV | Point of Sale / POS |
| Abertura de caixa / Fechamento de caixa | POS Opening Entry / POS Closing Entry |
| Venda | POS Invoice |
| Nota de venda | Sales Invoice |
| Cliente | Customer |
| Fornecedor | Supplier |
| Movimentação de estoque | Stock Entry |
| Pedido de reposição | Material Request |
| Lote | Batch |
| Validade | Expiry / Expiry Date |
| Empresa | Company |
| Centro de custo | Cost Center |
| Fabricação | Manufacturing |
| Posto de fabricação | Workstation |

Para incluir ou corrigir um nome, edite `flor_de_lotus/nomenclature.py` e rode:

```bash
python -m flor_de_lotus.build_assets
```

Isso atualiza `flor_de_lotus/translations/pt-BR.csv`. Atualize também a tabela de [GLOSSARIO.md](GLOSSARIO.md): a conferência do app exige que as duas listas sejam iguais. O Frappe lê esse CSV direto (não precisa virar arquivo gettext). As traduções ficam em cache, então depois da troca rode `bench --site SEU_SITE clear-cache` e atualize a página.

O arquivo é `pt-BR.csv`. O idioma `pt` (português genérico) não usa esta lista.

## O que esta versão não faz

- Não cria loja, usuário de função, produto, vela, estoque, PDV nem fabricação.
- Não mexe em arquivo nenhum dentro de `erpnext/`.
- Não trata de nota fiscal, NFC-e ou NF-e.

O módulo técnico se chama **Flor de Lotus**, sem acento, porque a pasta do módulo segue esse nome. O título que aparece para a pessoa é **Flor de Lótus**.

## Conferir o app sem um site

Na pasta `apps/flor_de_lotus`, com o Python enxergando o pacote:

```bash
PYTHONPATH=. python -m flor_de_lotus.self_check
```

Isso importa o pacote, confere ganchos, paleta, SVG provisório, CSV e glossário. Não substitui um `bench --site … install-app`.
