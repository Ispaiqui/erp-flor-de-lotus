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
)


def render_translations_csv() -> str:
	buffer = io.StringIO(newline="")
	writer = csv.writer(buffer, lineterminator="\n", quoting=csv.QUOTE_ALL)
	for source, translation, _note in TERMS:
		writer.writerow([source, translation, ""])
	return buffer.getvalue()
