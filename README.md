# ERPZ Transporte — Gestão de Expedição, Cargas e Faturamento Logístico

Solução corporativa de **Expedição, Gestão de Cargas e Logística de Transporte** desenvolvida nativamente para o **Frappe Framework** e **ERPNext** (v16), permitindo agrupar múltiplos Pedidos de Venda em Romaneios de Carga consolidados, dimensionar veículos, calcular cubagem ($m^3$) e pesos, faturar em lote gerando NF-e e emitir documentos oficiais de transporte.

---

## Sumário Executivo

O **ERPZ Transporte** atende o elo crítico entre o fechamento comercial e a entrega física das mercadorias aos clientes:
1. **Montagem de Cargas (Romaneios)**: Agrupamento inteligente de pedidos de venda por rota, transportadora, veículo e capacidade.
2. **Dimensionamento de Carga e Cubagem**: Cálculo automático de peso líquido total, peso bruto, quantidade de volumes e cubagem ($m^3$) com base nos cadastros dos itens.
3. **Indicadores de Ocupação e Prevenção de Sobrecarga**: Barras visuais e percentuais de ocupação de peso e volume em relação à capacidade útil do veículo.
4. **Faturamento em Lote e Emissão de NF-e**: Faturamento simultâneo de todos os pedidos da carga com geração direta dos Documentos Fiscais Eletrônicos (`Documento Fiscal Eletronico`).
5. **3 Formatos Oficiais de Impressão de Romaneio**: Sintético, Analítico com Produtos e Mapa de Baú (ordem de carregamento).
6. **Relatório de Cargas e Faturamento**: Visão gerencial do status de carregamento, motorista, placa, rota e valores faturados.

---

## 1. Arquitetura e Modelo de Dados

O aplicativo estrutura os dados em DocTypes nativos do Frappe:

| DocType | Tipo | Finalidade |
| :--- | :--- | :--- |
| **`Montagem de Carga`** | Principal | Registro do romaneio de carga (`CARGA-.YYYY.-.#####`). Armazena data de saída prevista, veículo, motorista, transportadora, rota, peso bruto total, cubagem ($m^3$), % de ocupação e status (*Planejada, Carregada, Faturada, Em Trânsito, Entregue*). |
| **`Item Montagem de Carga`** | Tabela Filha | Pedidos de venda vinculados à carga, com cliente, endereço de entrega, valor do pedido, peso líquido, peso bruto, volumes e documento fiscal gerado. |
| **`Veiculo Transporte`** | Cadastro | Cadastro da frota de veículos (caminhões, carretas, vans). Armazena placa, UF da placa, modelo, tara (kg), capacidade de carga útil (kg) e volume cúbico útil ($m^3$). |

---

## 2. Dimensionamento Físico e Cubagem Automática

A partir dos campos customizados criados nos itens do ERPNext (`peso_liquido`, `peso_bruto` e dimensões volumétricas), a Montagem de Carga realiza a soma e validação automática:

$$	ext{Peso Bruto Total} = \sum (	ext{Quantidade} 	imes 	ext{Peso Bruto do Item})$$
$$	ext{Cubagem Total } (m^3) = \sum \left(rac{	ext{Altura} 	imes 	ext{Largura} 	imes 	ext{Comprimento}}{1.000.000}ight) 	imes 	ext{Quantidade}$$
$$	ext{Ocupação de Peso (\%)} = \left(rac{	ext{Peso Bruto Total}}{	ext{Capacidade Útil do Veículo}}ight) 	imes 100$$
$$	ext{Ocupação Volumétrica (\%)} = \left(rac{	ext{Cubagem Total } m^3}{	ext{Volume Útil do Baú } m^3}ight) 	imes 100$$

* O sistema emite alerta visual quando a carga excede a capacidade máxima legal permitida para o veículo cadastrado.

---

## 3. Faturamento em Lote de Pedidos de Venda

Com a carga conferida e liberada para despacho:
1. O usuário aciona o botão **`Faturar Carga em Lote`**.
2. O sistema itera sobre cada Pedido de Venda (`Sales Order`) da carga que ainda não foi faturado.
3. Cria a `Sales Invoice` no ERPNext e gera o `Documento Fiscal Eletronico` (NF-e) com transmissão para a SEFAZ.
4. Vincula a chave de acesso, o número da nota e o protocolo de autorização na linha do romaneio.
5. Atualiza o status da carga para **Faturada**.

---

## 4. Três Formatos Oficiais de Impressão de Romaneio

A impressão da Montagem de Carga disponibiliza três layouts especializados:

1. **Formato Sintético**:
   * Resumo executivo da carga para conferência rápida de portaria e liberação de viagem.
   * Exibe dados do veículo, motorista, rota, quantidade total de pedidos, volumes e pesos consolidados.
2. **Formato Analítico com Produtos**:
   * Detalhamento linha a linha contendo cada Pedido de Venda, cliente, endereço completo de entrega, telefone, nota fiscal emitida e a relação completa de produtos, quantidades e pesos.
3. **Mapa de Baú / Ordem de Carregamento**:
   * Ordem de carregamento física planejada para facilitar a estiva: as primeiras entregas da rota são carregadas por último no baú (ordem LIFO - *Last-In, First-Out*), evitando remanejo de mercadorias no desembarque.

---

## 5. Relatório de Cargas e Faturamento

Relatório analítico em grade (*Script Report*) acessível no menu lateral **ERPZ Transporte &rarr; Relatório de Cargas e Faturamento**:
* Filtros por Período, Transportadora, Veículo e Situação da Carga.
* Visão consolidada de romaneios expedidos, valores de frete, peso transportado e faturamento total realizado.

---

## 6. Estrutura de Diretórios e Código-Fonte

```
erpz_transporte/
├── desktop_icon/
│   └── erpz_transporte.json       # Ícone oficial no Desk
├── erpz_transporte/
│   ├── doctype/
│   │   ├── montagem_de_carga/     # DocType de Romaneio, faturamento em lote e impressões
│   │   ├── item_montagem_de_carga/ # Linhas de pedidos de venda da carga
│   │   └── veiculo_transporte/    # Cadastro de veículos, tara, cubagem e capacidades
│   ├── report/
│   │   └── relatorio_de_cargas_e_faturamento/ # Script report de acompanhamento de cargas
│   ├── workspace/
│   │   └── erpz_transporte/       # Workspace com atalhos de expedição
│   └── workspace_sidebar/
│       └── erpz_transporte.json   # Menu lateral do módulo de transporte
├── hooks.py
├── setup.py                       # Inicialização e vinculações
└── pyproject.toml
```

---

## Licença

Distribuído sob licença MIT. Desenvolvido para o ecossistema ERPZ / Frappe Framework v16.
