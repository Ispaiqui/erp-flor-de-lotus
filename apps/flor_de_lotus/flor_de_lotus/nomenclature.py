# Copyright (c) 2026, Flor de Lótus and Contributors
# License: GNU General Public License v3. See license.txt

"""Nomes que a equipe da loja vê.

Cada item é (texto original do ERPNext, nome na operação, nota curta).
O original é a string exata do DocType, do campo ou do módulo — o
documento não é renomeado. A tradução vai para ``translations/pt-BR.csv``.

A nota aparece no glossário. As decisões de Depósito, Nota de venda e
PDV/Caixa estão escritas em GLOSSARIO.md.
"""

from __future__ import annotations

import csv
import io

# source, translation, note
TERMS: tuple[tuple[str, str, str], ...] = (
	("Item", "Produto", "Cadastro do que a loja vende ou guarda."),
	("Item Name", "Nome do produto", "Campo do cadastro."),
	("Item Code", "Código do produto", "Código interno do produto."),
	("Item Group", "Grupo de produto", "Categoria."),
	("Item Price", "Preço do produto", "Preço numa lista de preço."),
	("Price List", "Lista de preço", "Tabela de preços."),
	("UOM", "Unidade de medida", "Unidade de estoque e de venda."),
	("Barcode", "Código de barras", "Um código por produto, não por quantidade."),
	("Barcodes", "Códigos de barras", "Tabela de códigos no produto."),
	("Warehouse", "Depósito", "O lugar onde a mercadoria fica. Ver a decisão no glossário."),
	("Warehouse Type", "Tipo de depósito", ""),
	("Stock", "Estoque", "A quantidade e o módulo. Não é o lugar."),
	("Inventory", "Estoque", "Aba de estoque no cadastro do produto."),
	("Stock Entry", "Movimentação de estoque", "Documento de entrada, saída ou transferência."),
	("Stock Entry Type", "Tipo de movimentação", ""),
	("Stock Ledger Entry", "Lançamento de estoque", "Linha do razão. Não se edita à mão."),
	("Stock Reconciliation", "Contagem de inventário", ""),
	("Material Request", "Pedido de reposição", "Pedido da loja ao depósito central."),
	("Pick List", "Lista de separação", "Separação do pedido antes do envio."),
	("Material Receipt", "Entrada", "Tipo de movimentação: mercadoria que entra."),
	("Material Issue", "Saída", "Tipo de movimentação: mercadoria que sai."),
	("Material Transfer", "Transferência", "Tipo de movimentação entre depósitos."),
	(
		"Material Transfer for Manufacture",
		"Transferência para fabricação",
		"Insumo enviado ao setor de velas.",
	),
	("Manufacture", "Fabricação", "Tipo de movimentação que conclui a produção."),
	("Batch", "Lote", ""),
	("Batch No", "Número do lote", ""),
	("Has Batch No", "Controla lote", "Campo do produto."),
	("Expiry Date", "Validade", "Data de validade do lote."),
	("Expiry", "Validade", ""),
	("Has Expiry Date", "Controla validade", "Campo do produto."),
	("Shelf Life In Days", "Dias de validade", ""),
	("Manufacturing Date", "Data de fabricação", "Data em que o lote foi produzido."),
	("Customer", "Cliente", ""),
	("Customer Name", "Nome do cliente", ""),
	("Supplier", "Fornecedor", ""),
	("Supplier Name", "Nome do fornecedor", ""),
	("Sales Invoice", "Nota de venda", "Documento comercial. Não é nota fiscal."),
	("POS Invoice", "Venda", "Venda registrada no PDV."),
	("Point of Sale", "PDV", "Nome do ponto de venda no menu."),
	("Point Of Sale", "PDV", "Título da página de venda."),
	("POS", "PDV", ""),
	("POS Profile", "Perfil de PDV", "Um perfil por loja."),
	("POS Opening Entry", "Abertura de caixa", "Abre a sessão de quem opera o caixa."),
	("POS Closing Entry", "Fechamento de caixa", "Fecha a sessão de quem opera o caixa."),
	("Create POS Opening Entry", "Criar abertura de caixa", "Título do diálogo que abre o caixa no PDV."),
	("Opening Amount", "Valor de abertura", "Valor em cada forma de pagamento ao abrir o caixa."),
	("Opening Balance Details", "Detalhes da abertura", "Tabela de valores iniciais do caixa."),
	("Mode of Payment", "Forma de pagamento", ""),
	("Company", "Empresa", ""),
	("Cost Center", "Centro de custo", ""),
	("Employee", "Funcionário", ""),
	("Purchase Receipt", "Recebimento de compra", "Entrada vinda de uma compra."),
	("Manufacturing", "Fabricação", "Módulo do setor de velas."),
	("Workstation", "Posto de fabricação", "Onde a vela é produzida."),
	("Workstation Type", "Tipo de posto de fabricação", ""),
	("Work Order", "Ordem de produção", ""),
	("BOM", "Receita", "Insumos da vela. No ERPNext o documento se chama BOM."),
	("Job Card", "Cartão de fabricação", "Etapa da ordem, se for usada."),
	("Production Plan", "Plano de fabricação", ""),
	("Selling", "Vendas", "Módulo."),
	("Buying", "Compras", "Módulo."),
	# Tela de entrada do Frappe 17: o pt-BR oficial deixa estes textos vazios.
	("Sign In", "Entrar", "Título da tela de entrada."),
	(
		"Welcome! Please sign in to continue.",
		"Bem-vindo! Entre para continuar.",
		"Subtítulo da tela de entrada.",
	),
	("Forgot password?", "Esqueceu a senha?", "Link da tela de entrada."),
	("Send Link", "Enviar link", "Botão de entrada por link de e-mail."),
	("Email", "E-mail", "Rótulo do campo na tela de entrada. O pt-BR do Frappe deixa E-Mail."),
	# Textos vazios no pt-BR que aparecem nas telas pedidas.
	("Begin typing for results.", "Comece a digitar para ver os resultados.", "Campo de busca do link."),
	(
		"Clear the filters to see all records.",
		"Limpe os filtros para ver todos os registros.",
		"Lista vazia com filtro ativo.",
	),
	("Has Variants", "Tem variantes", "Filtro da lista de produtos."),
	("Batch Description", "Descrição do lote", "Campo do lote."),
	("Use Batch-wise Valuation", "Avaliar por lote", "Campo do lote."),
	("Tools", "Ferramentas", "Grupo do menu lateral."),
	("Serial & Batch", "Série e lote", "Grupo do menu lateral de estoque."),
	("Documentation", "Documentação", "Link no rodapé da lista."),
	(
		"Show all (including disabled)",
		"Mostrar todos (inclusive desativados)",
		"Filtro da árvore de depósitos.",
	),
	("Expand/Collapse", "Expandir/recolher", "Ação da árvore de depósitos."),
	("Reports", "Relatórios", "O pt-BR do Frappe deixa esta palavra em minúsculas."),
	(
		"All Warehouses",
		"Todos os depósitos",
		"Nome do depósito raiz criado na instalação. O pt-BR do ERPNext usa Armazéns.",
	),
	("{0} Tree", "Árvore de {0}", "Título da visualização em árvore."),
	# Início: o quadro de boas-vindas do ERPNext ainda está em inglês no pt-BR.
	("Good morning", "Bom dia", "Saudação da página Início."),
	("Good afternoon", "Boa tarde", "Saudação da página Início."),
	("Good evening", "Boa noite", "Saudação da página Início."),
	("Get to know ERPNext", "Conheça o Flor de Lótus", "Título do quadro de início. O original cita o ERPNext."),
	("{0} of {1} steps done", "{0} de {1} passos feitos", "Progresso do quadro de início."),
	("Invite your team", "Convide a equipe", "Passo do quadro de início."),
	(
		"Add the people you work with and choose what they can see.",
		"Adicione quem trabalha com você e escolha o que cada pessoa pode ver.",
		"Texto do convite no quadro de início.",
	),
	("Get your books ready", "Deixe as contas prontas", "Passo de contas no quadro de início."),
	("Make your first sale", "Faça a primeira venda", "Passo de vendas no quadro de início."),
	("Order from your suppliers", "Peça aos fornecedores", "Passo de compras no quadro de início."),
	("Keep track of your stock", "Acompanhe o estoque", "Passo de estoque no quadro de início."),
	("Plan and run production", "Planeje a fabricação", "Passo de fabricação no quadro de início."),
	("Plan and deliver projects", "Planeje e entregue os projetos", "Passo de projetos no quadro de início."),
	("Track what your business owns", "Acompanhe o que a empresa tem", "Passo de ativos no quadro de início."),
	("Keep quality in check", "Cuide da qualidade", "Passo de qualidade no quadro de início."),
	(
		"Your income and expenses over the year, and what's left as profit.",
		"Receitas e despesas do ano, e o que sobra de lucro.",
		"Texto do gráfico de lucro e perdas no Início.",
	),
	("Annual Sales", "Vendas no ano", "Cartão do Início."),
	("Annual Purchase", "Compras no ano", "Cartão do Início."),
	("Total Stock Value", "Valor total do estoque", "Cartão do Início."),
	(
		"If enabled, the system will allow negative stock entries for this batch, overriding the 'Allow negative stock for Batch' setting in Stock Settings. This may lead to incorrect valuation rates, so it is recommended to avoid using this option.",
		"Se marcado, este lote pode ficar com estoque negativo, mesmo com a trava das configurações de estoque. Isso pode distorcer o custo. Evite usar.",
		"Ajuda do campo de estoque negativo no lote.",
	),
	("Variant Of", "Variante de", "Coluna da lista de produtos."),
	("Serial No", "Número de série", "Documento e item do menu de estoque."),
	("Serial and Batch Bundle", "Pacote de série e lote", "Documento e item do menu de estoque."),
	("Access", "Acesso", "Item de menu que o idioma do Frappe ainda deixava em inglês."),
)


def render_translations_csv() -> str:
	buffer = io.StringIO(newline="")
	writer = csv.writer(buffer, lineterminator="\n", quoting=csv.QUOTE_ALL)
	for source, translation, _note in TERMS:
		writer.writerow([source, translation, ""])
	return buffer.getvalue()
