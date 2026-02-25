import sys
sys.path.append('backend')
import export

mock_data = {
    'data_precificacao': '24/02/2026', 'protocolo': '24022026-123',
    'nome_cliente': 'Teste', 'nome_equipamento': 'Eq', 'quantidade': 1,
    'valor_tabela': 1000.0, 'frete_tipo': 'FOB', 'comissao_representante': False,
    'estado_destino': 'SP', 'margem_negociacao_perc': 10.0,
}

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

buffer = io.BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=letter)

# Let's reproduce exactly what export.py does for data:
frete_str = "FOB"
comissao_str = "Não"

data = [
    ["Data da Precificação", str(mock_data.get('data_precificacao', ''))],
    ["Protocolo", str(mock_data.get('protocolo', 'N/A'))],
    ["Cliente", str(mock_data.get('nome_cliente', ''))],
    ["Equipamento", str(mock_data.get('nome_equipamento', ''))],
    ["Quantidade", str(mock_data.get('quantidade', ''))],
    ["Tabela Base (+ Frete se CIF)", "1000"],
    ["Frete (Informativo)", frete_str],
    ["Comissão Representante", comissao_str],
    ["Subtotal Com Comissão", "100"],
    ["Margem Negociação", "10"],
    ["Subtotal Com Margem (Base Cálculo)", "100"],
    ["Destino", "SP"],
    ["Valor do Imposto (DIFAL)", "10"],
    ["VALOR CHEIO DE VENDA", "10"],
    ["Valor Mínimo (Reserva)", "10"],
    ["Desconto Concedido (%)", "10"],
    ["", ""],
    ["Valor Unitário Final", "10"],
    ["Valor Total Final", "10"]
]

for i, row in enumerate(data):
    if len(row) != 2:
        print(f"ROW {i} DOES NOT HAVE 2 ELEMENTS: {row}")

# Now build the table:
table = Table(data)
# Copy the exact style that caused the crash in export.py
table_style = TableStyle([
    ('BACKGROUND', (0, 0), (0, 18), colors.HexColor('#e5e7eb')), # Light Gray column 1
    ('TEXTCOLOR', (0, 0), (1, 18), colors.HexColor('#1f2937')),
    ('ALIGN', (0, 0), (1, 18), 'LEFT'),
    ('FONTNAME', (0, 0), (0, 18), 'Helvetica-Bold'), # Bold col 1
    ('FONTNAME', (1, 0), (1, 18), 'Helvetica'), # Normal col 2
    ('FONTSIZE', (0, 0), (1, 18), 11),
    ('BOTTOMPADDING', (0, 0), (1, 18), 10),
    ('TOPPADDING', (0, 0), (1, 18), 10),
    ('GRID', (0, 0), (1, 18), 1, colors.black),
    # Highlight Results
    ('BACKGROUND', (0, 15), (1, 18), colors.HexColor('#f1f5f9')), 
    ('BACKGROUND', (0, 17), (1, 17), colors.HexColor('#e0f2fe')), # Unitario
    ('BACKGROUND', (0, 18), (1, 18), colors.HexColor('#dbeafe')), # Total
    ('FONTNAME', (1, 15), (1, 18), 'Helvetica-Bold'), # Bold results values
    # Remove border on blank row
    ('LINEBELOW', (0, 16), (1, 16), 0, colors.white),
    ('LINEABOVE', (0, 16), (1, 16), 0, colors.white),
    ('GRID', (0, 16), (1, 16), 0, colors.white),
    ('BACKGROUND', (0, 16), (1, 16), colors.white),
])
table.setStyle(table_style)
try:
    doc.build([table])
    print("SUCCESS MOCK REPRODUCTION")
except Exception as e:
    import traceback
    traceback.print_exc()

import export
try:
    export.export_to_pdf(mock_data)
    print("SUCCESS EXPORT.PY")
except Exception as e:
    import traceback
    traceback.print_exc()

