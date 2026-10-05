# Glossário — Flor de Lótus

Nomes que a equipe da loja vê, e o texto original do ERPNext. Os documentos não foram renomeados. A troca está em `flor_de_lotus/translations/pt-BR.csv` e só aparece quando o idioma do usuário é **português do Brasil** (`pt-BR`).

Isto é vocabulário, não regra de negócio. Loja, caixa, velas e permissões ainda não existem neste app.

## Depósito, e não Estoque, para Warehouse

**Warehouse → Depósito.**

Estoque é a quantidade: o que entra, o que sai e o saldo. O Warehouse é o lugar onde essa quantidade fica — o central, o de cada loja, o de trânsito e os da fabricação. Chamar o lugar de Estoque misturaria o endereço com o saldo.

A especificação também chama esse lugar de armazém. Aqui o nome da tela é Depósito, que foi a opção pedida para a equipe. Armazém continua valendo na conversa como sinônimo. O módulo Stock segue como Estoque.

## Nota de venda, e Venda para o que sai no PDV

**Sales Invoice → Nota de venda.** **POS Invoice → Venda.**

A operação chama de venda o que acontece no caixa. No ERPNext isso pode ser um POS Invoice ou, quando o movimento vira documento comercial, uma Sales Invoice. Venda fica no documento do PDV. Nota de venda fica na Sales Invoice, para não parecer a mesma tela.

Nota de venda não é nota fiscal. Documento fiscal (NFC-e, NF-e) fica para uma versão futura e não tem nome nesta lista.

## PDV na tela, Caixa na sessão

**Point of Sale / POS → PDV.** **Abertura e fechamento → Caixa.**

PDV é a tela em que se lê o código e se registra a venda. Caixa é a sessão de quem está operando: abertura (`POS Opening Entry`) e fechamento (`POS Closing Entry`). A função da pessoa também se chama Caixa. Os dois nomes ficam, cada um no seu lugar.

## Fabricação

O módulo Manufacturing e o tipo de movimento Manufacture aparecem como **Fabricação**. Workstation vira **Posto de fabricação**, para não usar a mesma palavra para o setor e para o lugar onde a vela é feita. A BOM, no vocabulário das velas, é **Receita**.

## Lista

| Termo na operação | Original no ERPNext | Nota |
| --- | --- | --- |
| Produto | Item | Cadastro do que a loja vende ou guarda. |
| Nome do produto | Item Name | Campo do cadastro. |
| Código do produto | Item Code | Código interno do produto. |
| Grupo de produto | Item Group | Categoria. |
| Preço do produto | Item Price | Preço numa lista de preço. |
| Lista de preço | Price List | Tabela de preços. |
| Unidade de medida | UOM | Unidade de estoque e de venda. |
| Código de barras | Barcode | Um código por produto, não por quantidade. |
| Códigos de barras | Barcodes | Tabela de códigos no produto. |
| Depósito | Warehouse | O lugar onde a mercadoria fica. Ver a decisão no glossário. |
| Tipo de depósito | Warehouse Type |  |
| Estoque | Stock | A quantidade e o módulo. Não é o lugar. |
| Estoque | Inventory | Aba de estoque no cadastro do produto. |
| Movimentação de estoque | Stock Entry | Documento de entrada, saída ou transferência. |
| Tipo de movimentação | Stock Entry Type |  |
| Lançamento de estoque | Stock Ledger Entry | Linha do razão. Não se edita à mão. |
| Contagem de inventário | Stock Reconciliation |  |
| Pedido de reposição | Material Request | Pedido da loja ao depósito central. |
| Lista de separação | Pick List | Separação do pedido antes do envio. |
| Entrada | Material Receipt | Tipo de movimentação: mercadoria que entra. |
| Saída | Material Issue | Tipo de movimentação: mercadoria que sai. |
| Transferência | Material Transfer | Tipo de movimentação entre depósitos. |
| Transferência para fabricação | Material Transfer for Manufacture | Insumo enviado ao setor de velas. |
| Fabricação | Manufacture | Tipo de movimentação que conclui a produção. |
| Lote | Batch |  |
| Número do lote | Batch No |  |
| Controla lote | Has Batch No | Campo do produto. |
| Validade | Expiry Date | Data de validade do lote. |
| Validade | Expiry |  |
| Controla validade | Has Expiry Date | Campo do produto. |
| Dias de validade | Shelf Life In Days |  |
| Data de fabricação | Manufacturing Date | Data em que o lote foi produzido. |
| Cliente | Customer |  |
| Nome do cliente | Customer Name |  |
| Fornecedor | Supplier |  |
| Nome do fornecedor | Supplier Name |  |
| Nota de venda | Sales Invoice | Documento comercial. Não é nota fiscal. |
| Venda | POS Invoice | Venda registrada no PDV. |
| PDV | Point of Sale | Nome do ponto de venda no menu. |
| PDV | Point Of Sale | Título da página de venda. |
| PDV | POS |  |
| Perfil de PDV | POS Profile | Um perfil por loja. |
| Abertura de caixa | POS Opening Entry | Abre a sessão de quem opera o caixa. |
| Fechamento de caixa | POS Closing Entry | Fecha a sessão de quem opera o caixa. |
| Forma de pagamento | Mode of Payment |  |
| Empresa | Company |  |
| Centro de custo | Cost Center |  |
| Funcionário | Employee |  |
| Recebimento de compra | Purchase Receipt | Entrada vinda de uma compra. |
| Fabricação | Manufacturing | Módulo do setor de velas. |
| Posto de fabricação | Workstation | Onde a vela é produzida. |
| Tipo de posto de fabricação | Workstation Type |  |
| Ordem de produção | Work Order |  |
| Receita | BOM | Insumos da vela. No ERPNext o documento se chama BOM. |
| Cartão de fabricação | Job Card | Etapa da ordem, se for usada. |
| Plano de fabricação | Production Plan |  |
| Vendas | Selling | Módulo. |
| Compras | Buying | Módulo. |

A marca desta versão (logo e cores) é provisória. A licença do app é a GPL-3.0.
