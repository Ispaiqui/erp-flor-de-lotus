# Flor de Lótus

Camada de produto para a operação da Flor de Lótus: cinco lojas, um depósito central, PDV e fabricação de velas, em cima do ERPNext.

A **V1** traz lojas, funções, catálogo de demonstração e a trava de acesso por loja no servidor. A marca e os nomes em português continuam neste app. O núcleo do ERPNext não é editado.

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

A migração (`bench --site SEU_SITE migrate`, também chamada pelo `install-app`) cria o DocType **Loja**, as cinco funções, os quadros e — se a empresa **Flor de Lótus** já existir — a carga de demonstração. Sem essa empresa, a carga espera: rode o assistente da empresa e migre de novo. A carga pode rodar outra vez; ela não duplica loja, produto nem usuário.

Para repetir só a carga, com a empresa já no site:

```bash
bench --site SEU_SITE execute flor_de_lotus.setup_v1.seed_v1
bench --site SEU_SITE clear-cache
```

O usuário também precisa estar em português do Brasil para ver os nomes da lista. Em **System Settings**, idioma `pt-BR`. Saia e entre de novo, e atualize a página sem cache.

Quem ainda não entrou vê a tela de entrada no idioma do site, e não no idioma do navegador. Um Chrome em inglês, com o site em `pt-BR`, abre em português. Se a pessoa escolher outro idioma (cookie `preferred_language` ou `?_lang=`), essa escolha vale.

Para repor a marca provisória depois de um teste:

```bash
bench --site SEU_SITE execute flor_de_lotus.install.apply_branding --kwargs "{'overwrite': True}"
bench --site SEU_SITE clear-cache
```

`overwrite` troca também um logo que você já tenha colocado. Sem isso, uma migração não desfaz a sua escolha.

O `--kwargs` do `bench execute` é código Python, não JSON. Use `{'overwrite': True}`. `{"overwrite": true}` quebra com `NameError`, porque `true` não existe no Python.

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

## O que a V1 faz

- DocType **Loja**: depósito, centro de custo, perfil de PDV, gerente, endereço. CNPJ, inscrição estadual e endereço fiscal existem e ficam vazios ou só com o texto do endereço, até a definição fiscal.
- Árvore de depósitos: Central, grupo Lojas com Loja 1 a Loja 5, trânsito, e o grupo Fabricação (insumos e velas acabadas) separado do central.
- Cinco funções, cada uma com um perfil de função: Dono, Gerente da loja, Caixa, Estoquista, Fabricação.
- Ao gravar o usuário com loja, o servidor cria User Permission de Loja, depósito, centro de custo e perfil de PDV.
- Funcionário com loja. O gerente só grava funcionário e usuário da própria loja.
- Catálogo: grupos, unidade **Unidade**, lista **Varejo Flor de Lótus** (um preço para as cinco lojas) e 18 produtos. O campo `catalogo` separa Produto e Vela. Três itens são vela, só para a função Fabricação não cair numa lista vazia.
- Quadros iniciais diferentes para Dono, Gerente da loja e Caixa. Estoquista e Fabricação têm função e menu filtrado, sem quadro próprio.
- Teste de servidor: gerente e caixa da loja 1 não leem nem gravam a loja 2.

Senha de todos os usuários de demonstração: `FlorDemo2026`. Idioma `pt-BR`, fuso `America/Sao_Paulo`.

| Pessoa | E-mail | Função | Loja |
| --- | --- | --- | --- |
| Helena | `dono@flor.localhost` | Dono | todas |
| Marina | `gerente.loja1@flor.localhost` | Gerente da loja | Flor de Lótus Loja 1 |
| Beatriz | `gerente.loja2@flor.localhost` | Gerente da loja | Flor de Lótus Loja 2 |
| Ana | `caixa.loja1@flor.localhost` | Caixa | Flor de Lótus Loja 1 |
| Camila | `caixa.loja2@flor.localhost` | Caixa | Flor de Lótus Loja 2 |
| Pedro | `estoquista@flor.localhost` | Estoquista | depósito Central |
| Lúcia | `fabricacao@flor.localhost` | Fabricação | insumos e velas acabadas |

O dono entra no quadro **Dono**. O gerente entra em **Gerente da loja**. O caixa entra em **Caixa**.

## O que ficou para as versões seguintes

- V2: código de barras, movimentação, motivo obrigatório, lote, validade, contagem.
- V3: falta, pedido de segunda, separação, transferência com trânsito e recebimento.
- V4: grade do PDV, venda, pagamento (PIX, cartão, crediário) e baixa de estoque. O perfil de PDV da V1 é só o vínculo, com dinheiro e conta de abatimento.
- V5: catálogo de velas de verdade, receita, ordem de produção, venda a granel.
- V6: nota fiscal, NFC-e, NF-e. CNPJ por loja ou um só continua em aberto.
- V7: lucro por loja e consolidado. O quadro do dono nesta versão não é esse painel.
- V8: alertas e pedidos automáticos.

O módulo técnico se chama **Flor de Lotus**, sem acento, porque a pasta do módulo segue esse nome. O título que aparece para a pessoa é **Flor de Lótus**. Nada em `erpnext/` foi alterado.

## Adaptações em relação à especificação

- O ERPNext já tinha criado o depósito folha **Lojas**. Ele virou o grupo das cinco lojas. O depósito padrão da empresa passou a ser **Central**, porque um grupo não pode ser o depósito padrão.
- O depósito de trânsito mantém o nome que a instalação deu (**Mercadorias Em Trânsito**), com tipo Transit.
- Trabalho em andamento e produtos acabados, criados pela instalação, ficaram debaixo do grupo Fabricação.
- Os nomes de depósito e centro de custo ganham o sufixo da empresa (` - FDL`). É a regra do ERPNext.
- User Permission de depósito e de centro de custo vale só para aquele documento. Se valesse para todo vínculo, a empresa sumia da tela, porque ela aponta para o depósito padrão. Loja e perfil de PDV limitam funcionário, usuário e sessão de caixa.
- Os quadros são gravados na migração, em Python, e não em arquivo JSON. As funções ainda não existem quando o Frappe importa JSON.
- Preço igual nas cinco lojas, numa lista só. O dono ainda não escolheu preço por loja.
- A função Fabricação só lista item com catálogo Vela. Estoquista e fabricação não têm loja: o estoquista fica no Central, a fabricação nos dois depósitos dela.
- O quadro Início do ERPNext, com lucro e perda, pede a função Desk User. Os usuários de demonstração não têm essa função, então caem no quadro da função deles.

## Conferir o app sem um site

Na pasta `apps/flor_de_lotus`, com o Python enxergando o pacote:

```bash
PYTHONPATH=. python -m flor_de_lotus.self_check
```

Isso importa o pacote, confere ganchos, paleta, SVG provisório, CSV e glossário. Não substitui um `bench --site … install-app`.
