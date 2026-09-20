# ERPZ Transporte — Gestão de Expedição, Cargas, CT-e 4.0, MDF-e 3.0 e Logística

Solução corporativa de **Expedição, Gestão de Cargas, TMS e Documentos Eletrônicos de Transporte** desenvolvida nativamente para o **Frappe Framework** e **ERPNext** (v16), permitindo agrupar múltiplos Pedidos de Venda em Romaneios de Carga consolidados, dimensionar veículos, calcular cubagem ($m^3$) e pesos, faturar em lote gerando NF-e e emitir documentos oficiais de transporte: **CT-e 4.00 (Conhecimento de Transporte Eletrônico)** com DACTE e **MDF-e 3.00a (Manifesto Eletrônico de Documentos Fiscais)** com DAMDFE e encerramento de viagem.

---

## Sumário Executivo

O **ERPZ Transporte** atende o elo crítico entre o fechamento comercial, o faturamento e a entrega física das mercadorias aos clientes:
1. **Montagem de Cargas (Romaneios)**: Agrupamento inteligente de pedidos de venda por rota, transportadora, veículo e capacidade.
2. **Dimensionamento de Carga e Cubagem**: Cálculo automático de peso líquido total, peso bruto, quantidade de volumes e cubagem ($m^3$) com base nos cadastros dos itens.
3. **Indicadores de Ocupação e Prevenção de Sobrecarga**: Barras visuais e percentuais de ocupação de peso e volume em relação à capacidade útil do veículo.
4. **Faturamento em Lote e Emissão de NF-e**: Faturamento simultâneo de todos os pedidos da carga com geração direta dos Documentos Fiscais Eletrônicos (`Documento Fiscal Eletronico`).
5. **3 Formatos Oficiais de Impressão de Romaneio**: Sintético (portaria), Analítico com Produtos (conferência) e Mapa de Baú (ordem de carregamento LIFO).
6. **Conhecimento de Transporte Eletrônico (CT-e Mod. 57)**: Emissão do CT-e 4.00 rodoviário para cobrança de frete, com cálculo de ICMS sobre frete, transmissão via WebService e geração do **DACTE em PDF**.
7. **Manifesto Eletrônico de Documentos Fiscais (MDF-e Mod. 58)**: Emissão do MDF-e 3.00a para transporte interestadual / intermunicipal (prestador de serviço ou carga própria), vinculação das NF-e/CT-e transportadas, apólice de seguro de carga (RCTR-C), geração do **DAMDFE com QR Code** e evento oficial de **Encerramento de Viagem (`110112`)**.
8. **Relatório de Cargas e Faturamento**: Visão gerencial do status de carregamento, motorista, placa, rota e valores faturados.

---

## 1. Arquitetura e Modelo de Dados

O aplicativo estrutura os dados em DocTypes nativos do Frappe:

| DocType | Tipo | Finalidade |
| :--- | :--- | :--- |
| **`Montagem de Carga`** | Principal | Registro do romaneio de carga (`CARGA-.YYYY.-.#####`). Armazena data de saída prevista, veículo, motorista, transportadora, rota, peso bruto total, cubagem ($m^3$), % de ocupação e status (*Planejada, Carregada, Faturada, Em Trânsito, Entregue*). |
| **`Item Montagem de Carga`** | Tabela Filha | Pedidos de venda vinculados à carga, com cliente, endereço de entrega, valor do pedido, peso líquido, peso bruto, volumes e documento fiscal gerado. |
| **`Veiculo Transporte`** | Cadastro | Cadastro da frota de veículos (caminhões, carretas, vans). Armazena placa, UF da placa, modelo, tara (kg), capacidade de carga útil (kg) e volume cúbico útil ($m^3$). |
| **`Motorista Transporte`** | Cadastro | Cadastro dos motoristas, CPF, CNH e categoria de habilitação. |
| **`Conhecimento de Transporte`** | Frete | Emissão do CT-e 4.00 (Mod. 57) com cálculo de frete valor, pedágio, ICMS frete, amarração de NF-e e impressão do DACTE em PDF. |
| **`Manifesto Eletronico Documentos`** | Manifesto | Emissão do MDF-e 3.00a (Mod. 58) com dados do veículo, condutor, seguro da carga, transmissão SEFAZ, impressão do DAMDFE e evento de Encerramento. |

---

## 2. Emissão de CT-e (Modelo 57) e DACTE

Para empresas que realizam prestação de serviço de transporte de cargas:
* Emissão no leiaute nacional CT-e 4.00 com modal rodoviário (`01 - Rodoviário`).
* Componentes do frete: Frete Peso, Frete Valor, Pedágio e Taxas de Despacho.
* Apuração do ICMS do frete (CST 00, 20, 40, 60, 90).
* Assinatura digital com Certificado Digital A1 via XMLDSig.
* Transmissão para o WebService `cteAutorizacao` da SEFAZ estadual.
* Geração do **DACTE (Documento Auxiliar do CT-e)** em PDF com código de barras Code128.

---

## 3. Emissão de MDF-e (Modelo 58) e DAMDFE

Obrigatório para o transporte de cargas fracionadas ou lotação entre municípios/estados:
* Tipo de emitente configurável: **1 - Prestador de Serviço de Transporte** ou **2 - Transportador de Carga Própria** (empresas industriais e comerciais que transportam seus próprios produtos).
* Amarração automática de todas as chaves de acesso das NF-e transportadas no romaneio.
* Dados obrigatórios da apólice de seguro de carga (Seguradora, CNPJ e Número da Apólice RCTR-C).
* Geração do **DAMDFE oficial com QR Code** para fiscalização em postos fiscais de rodovias.
* Botão de **Encerramento de Viagem na SEFAZ** (Evento `110112`), liberando o veículo e motorista para a próxima viagem.

---

## 4. Dimensionamento Físico e Cubagem Automática

A partir dos campos customizados criados nos itens do ERPNext (`peso_liquido`, `peso_bruto` e dimensões volumétricas), a Montagem de Carga realiza a soma e validação automática:

$$	ext{Peso Bruto Total} = \sum (	ext{Quantidade} 	imes 	ext{Peso Bruto do Item})$$
$$	ext{Cubagem Total } (m^3) = \sum \left(rac{	ext{Altura} 	imes 	ext{Largura} 	imes 	ext{Comprimento}}{1.000.000}ight) 	imes 	ext{Quantidade}$$
$$	ext{Ocupação de Peso (\%)} = \left(rac{	ext{Peso Bruto Total}}{	ext{Capacidade Útil do Veículo}}ight) 	imes 100$$
$$	ext{Ocupação Volumétrica (\%)} = \left(rac{	ext{Cubagem Total } m^3}{	ext{Volume Útil do Baú } m^3}ight) 	imes 100$$

* O sistema emite alerta visual quando a carga excede a capacidade máxima legal permitida para o veículo cadastrado.

---

## 5. Faturamento em Lote de Pedidos de Venda

Com a carga conferida e liberada para despacho:
1. O usuário aciona o botão **`Faturar Carga em Lote`**.
2. O sistema itera sobre cada Pedido de Venda (`Sales Order`) da carga que ainda não foi faturado.
3. Cria a `Sales Invoice` no ERPNext e gera o `Documento Fiscal Eletronico` (NF-e) com transmissão para a SEFAZ.
4. Vincula a chave de acesso, o número da nota e o protocolo de autorização na linha do romaneio.
5. Atualiza o status da carga para **Faturada**.

---

## 6. Três Formatos Oficiais de Impressão de Romaneio

1. **Formato Sintético**: Resumo executivo da carga para conferência rápida de portaria e liberação de viagem.
2. **Formato Analítico com Produtos**: Detalhamento linha a linha contendo cada Pedido de Venda, cliente, endereço completo de entrega, telefone, nota fiscal emitida e a relação completa de produtos, quantidades e pesos.
3. **Mapa de Baú / Ordem de Carregamento**: Ordem física planejada para facilitar a estiva: as primeiras entregas da rota são carregadas por último no baú (ordem LIFO - *Last-In, First-Out*).

---

## 7. Relatório de Cargas e Faturamento

Relatório analítico em grade (*Script Report*) acessível no menu lateral **ERPZ Transporte &rarr; Relatório de Cargas e Faturamento**:
* Filtros por Período, Transportadora, Veículo e Situação da Carga.
* Visão consolidada de romaneios expedidos, valores de frete, peso transportado e faturamento total realizado.

---

## 8. Estrutura de Diretórios e Código-Fonte

```
erpz_transporte/
├── desktop_icon/
│   └── erpz_transporte.json       # Ícone oficial no Desk
├── erpz_transporte/
│   ├── doctype/
│   │   ├── montagem_de_carga/     # DocType de Romaneio, faturamento em lote e cubagem
│   │   ├── item_montagem_de_carga/ # Linhas de pedidos de venda da carga
│   │   ├── veiculo_transporte/    # Cadastro de veículos, tara, cubagem e capacidades
│   │   ├── motorista_transporte/  # Cadastro de condutores e CNH
│   │   ├── conhecimento_de_transporte/ # CT-e 4.00, transmissão SEFAZ e DACTE
│   │   └── manifesto_eletronico_documentos/ # MDF-e 3.00a, DAMDFE e encerramento
│   ├── print_format/
│   │   ├── romaneio_de_carga_sintetico/
│   │   ├── romaneio_de_carga_analitico/
│   │   └── mapa_de_carregamento_consolidado/
│   ├── report/
│   │   └── relatorio_de_cargas_e_faturamento/ # Relatório de cargas expedidas
│   ├── workspace/
│   │   └── erpz_transporte/       # Workspace de logística
│   └── workspace_sidebar/
│       └── erpz_transporte.json   # Menu lateral do módulo de transporte
├── hooks.py
├── setup.py                       # Inicialização e vinculações
└── pyproject.toml
```

---

## Licença

Distribuído sob licença MIT. Desenvolvido para o ecossistema ERPZ / Frappe Framework v16.
