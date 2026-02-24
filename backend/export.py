import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def export_to_excel(history_data: dict) -> BytesIO:
    df = pd.DataFrame([history_data])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Precificação')
    output.seek(0)
    return output

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(value):
    return f"{value:.2f}%".replace(".", ",")

def export_to_pdf(history_data: dict, author_name: str = "Consultor") -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        alignment=1, # Center
        spaceAfter=30,
        fontSize=24,
        fontName="Helvetica-Bold"
    )

    info_style = ParagraphStyle(
        'InfoText',
        parent=styles['Normal'],
        alignment=2, # Right
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=20
    )
    
    elements.append(Paragraph("Resumo de Precificação Web", title_style))
    
    # Metadata
    gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Paragraph(f"Gerado por: {author_name} | Em: {gerado_em}", info_style))
    
    # Check Frete
    frete_str = hr_frete = ""
    if history_data.get('frete_tipo') == 'CIF':
        frete_str = f"{format_currency(history_data.get('valor_frete', 0.0))}"
    else:
        frete_str = "FOB (Por conta do cliente)"

    # Check Comissão
    comissao_str = ""
    if history_data.get('comissao_representante'):
        comissao_str = f"{format_percent(history_data.get('percentual_comissao', 0.0))} / {format_currency(history_data.get('valor_comissao', 0.0))}"
    else:
        comissao_str = "Não se aplica"
        
    data = [
        ["Data da Precificação", str(history_data.get('data_precificacao', ''))],
        ["Protocolo", str(history_data.get('protocolo', 'N/A'))],
        ["Cliente", str(history_data.get('nome_cliente', ''))],
        ["Equipamento", str(history_data.get('nome_equipamento', ''))],
        ["Quantidade", str(history_data.get('quantidade', ''))],
        ["Valor de Tabela", format_currency(history_data.get('valor_tabela', 0.0))],
        ["Margem para Negociação", f"{format_percent(history_data.get('margem_negociacao_perc', 0.0))} / {format_currency(history_data.get('valor_margem', 0.0))}"],
        ["Comissão Representante", comissao_str],
        ["Frete (Modalidade / Valor)", frete_str],
        ["Destino", f"{history_data.get('estado_destino', '')} - DIFAL: {format_percent(history_data.get('percentual_difal', 0.0))}"],
        ["", ""],
        ["Base de Cálculo", format_currency(history_data.get('base_calculo', 0.0))],
        ["Valor do Imposto (DIFAL)", format_currency(history_data.get('valor_difal', 0.0))],
        ["Valor Unitário Final", format_currency(history_data.get('venda_unitario', 0.0))],
        ["Valor Total Final", format_currency(history_data.get('venda_total', 0.0))]
    ]
    
    col_widths = [doc.width * 0.45, doc.width * 0.55]
    table = Table(data, colWidths=col_widths)
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')), # Light Gray column 1
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), # Bold col 1
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'), # Normal col 2
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Highlight Results
        ('BACKGROUND', (0, -4), (-1, -1), colors.HexColor('#f1f5f9')), 
        ('BACKGROUND', (0, -2), (-1, -2), colors.HexColor('#e0f2fe')), # Unitario
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dbeafe')), # Total
        ('FONTNAME', (1, -4), (1, -1), 'Helvetica-Bold'), # Bold results values
        # Remove border on blank row
        ('LINEBELOW', (0, 9), (1, 9), 0, colors.white),
        ('LINEABOVE', (0, 9), (1, 9), 0, colors.white),
        ('GRID', (0, 9), (-1, 9), 0, colors.white),
        ('BACKGROUND', (0, 9), (-1, 9), colors.white),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
