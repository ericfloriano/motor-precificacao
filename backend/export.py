import os
import pandas as pd
from io import BytesIO
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import models

def export_to_excel(history_data: dict) -> BytesIO:
    df = pd.DataFrame([history_data])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Precificação')
    output.seek(0)
    return output

def format_currency(value):
    val = value or 0.0
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percent(value):
    val = value or 0.0
    return f"{val:.2f}%".replace(".", ",")

def export_to_pdf(history_data: dict, author_name: str = "Consultor") -> BytesIO:
    buffer = BytesIO()
    
    # 16:9 Landscape page size: Width 792 pt (11 inches), Height 445.5 pt (6.1875 inches)
    pagesize = (792, 445.5)
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=pagesize, 
        rightMargin=30, 
        leftMargin=30, 
        topMargin=25, 
        bottomMargin=25
    )
    elements = []
    
    # Visuri Brand Palette Colors
    c_azul_visuri = colors.HexColor('#123C69')
    c_teal = colors.HexColor('#0F766E')
    c_slate = colors.HexColor('#0F172A')
    c_dark_navy = colors.HexColor('#182235')
    c_light_teal_bg = colors.HexColor('#ECFEFF')
    c_badge_bg = colors.HexColor('#CCFBF1')
    c_gray_pastel = colors.HexColor('#64748B')
    
    styles = getSampleStyleSheet()
    
    # Typography / Styles
    style_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=c_gray_pastel,
        leading=10,
        spaceAfter=1
    )
    
    style_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=c_dark_navy,
        leading=12,
        spaceAfter=6
    )
    
    style_val_highlight = ParagraphStyle(
        'MetaValHighlight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        textColor=c_teal,
        leading=12,
        spaceAfter=6
    )
    
    style_title = ParagraphStyle(
        'RightTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=c_azul_visuri,
        leading=14,
        spaceAfter=8,
        alignment=0
    )
    
    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white,
        leading=11
    )
    
    style_table_header_right = ParagraphStyle(
        'TableHeaderRight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white,
        leading=11,
        alignment=2
    )
    
    style_table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=c_dark_navy,
        leading=11
    )
    
    style_table_text_bold = ParagraphStyle(
        'TableTextBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=c_dark_navy,
        leading=11
    )
    
    style_table_text_right = ParagraphStyle(
        'TableTextRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=c_dark_navy,
        leading=11,
        alignment=2
    )
    
    # Red Warning style for Minimum Allowed Price
    style_table_text_warning = ParagraphStyle(
        'TableTextWarning',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor('#B91C1C'),
        leading=11
    )
    
    style_table_text_warning_right = ParagraphStyle(
        'TableTextWarningRight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor('#B91C1C'),
        leading=11,
        alignment=2
    )
    
    style_obs_title = ParagraphStyle(
        'ObsTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        textColor=c_slate,
        leading=11,
        spaceAfter=3
    )
    
    style_obs_text = ParagraphStyle(
        'ObsText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        textColor=c_dark_navy,
        leading=11
    )
    
    style_footer_text = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        textColor=c_gray_pastel,
        leading=9
    )

    # Resolve logo path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.normpath(os.path.join(current_dir, "..", "img", "logo-visuri-azul.png"))

    # ==========================================
    # 1. LEFT COLUMN FLOWABLES (Metadata & Logo)
    # ==========================================
    left_flowables = []
    
    # Logo
    if os.path.exists(logo_path):
        # original ratio is 1719/469 = 3.66. Width 110 pt -> Height 30 pt
        left_flowables.append(Image(logo_path, width=110, height=30))
    else:
        left_flowables.append(Paragraph("<b>VISURI</b>", ParagraphStyle('LogoFB', fontName='Helvetica-Bold', fontSize=20, textColor=c_azul_visuri)))
        
    left_flowables.append(Spacer(1, 12))
    
    # Format Date
    data_prec_raw = history_data.get('data_precificacao', 'N/A')
    data_prec_str = str(data_prec_raw)
    try:
        dt_parsed = datetime.strptime(data_prec_str.split(' ')[0], "%Y-%m-%d")
        data_prec_str = dt_parsed.strftime("%d/%m/%Y")
    except Exception:
        pass
        
    # Metadata Card (using a single-column table with a background color)
    meta_data = [
        [Paragraph("CLIENTE", style_label)],
        [Paragraph(str(history_data.get('nome_cliente', 'N/A')), style_val)],
        [Paragraph("EQUIPAMENTO", style_label)],
        [Paragraph(f"{history_data.get('nome_equipamento', 'N/A')} (x{history_data.get('quantidade', 1)})", style_val)],
        [Paragraph("PROTOCOLO COMERCIAL", style_label)],
        [Paragraph(str(history_data.get('protocolo', 'N/A')), style_val_highlight)],
        [Paragraph("DATA DA PRECIPICAÇÃO", style_label)],
        [Paragraph(data_prec_str, style_val)],
        [Paragraph("RESPONSÁVEL", style_label)],
        [Paragraph(str(author_name), style_val)]
    ]
    
    meta_table = Table(meta_data, colWidths=[310])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_teal_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, c_teal),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    left_flowables.append(meta_table)
    
    # Observations box
    obs = history_data.get('observacoes')
    if obs:
        left_flowables.append(Spacer(1, 10))
        obs_data = [
            [Paragraph("OBSERVAÇÕES ADICIONAIS", style_obs_title)],
            [Paragraph(str(obs), style_obs_text)]
        ]
        obs_table = Table(obs_data, colWidths=[310])
        obs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 0.5, c_gray_pastel),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        left_flowables.append(obs_table)

    # ==========================================
    # 2. RIGHT COLUMN FLOWABLES (Pricing Details)
    # ==========================================
    right_flowables = []
    
    right_flowables.append(Paragraph("DEMONSTRATIVO DE PRECIPICAÇÃO", style_title))
    
    # Frete Formatting
    if history_data.get('frete_tipo') == 'CIF':
        frete_str = format_currency(history_data.get('valor_frete') or 0.0)
    else:
        frete_str = "FOB (Por conta do cliente)"

    # Comissão Formatting
    if history_data.get('comissao_representante'):
        comissao_str = f"{format_percent(history_data.get('percentual_comissao') or 0.0)} ({format_currency(history_data.get('valor_comissao') or 0.0)})"
    else:
        comissao_str = "Não se aplica"
        
    # Margem Formatting
    margem_str = f"{format_percent(history_data.get('margem_negociacao_perc') or 0.0)} ({format_currency(history_data.get('valor_margem') or 0.0)})"
    
    # DIFAL Formatting
    difal_str = f"{history_data.get('estado_destino', 'MG')} - {format_percent(history_data.get('percentual_difal') or 0.0)} ({format_currency(history_data.get('valor_difal') or 0.0)})"
    
    # Calculations
    venda_cheio = history_data.get('valor_venda_cheio') or 0.0
    minimo_venda = history_data.get('valor_minimo_venda') or 0.0
    if venda_cheio > 0:
        desconto_maximo_perc = ((venda_cheio - minimo_venda) / venda_cheio) * 100.0
    else:
        desconto_maximo_perc = 0.0

    # Desconto Formatting
    desconto_val = venda_cheio * ((history_data.get('desconto_concedido_perc') or 0.0) / 100.0)
    desconto_str = f"{format_percent(history_data.get('desconto_concedido_perc') or 0.0)} (- {format_currency(desconto_val)})"

    pricing_table_data = [
        [Paragraph("Item / Métrica de Custo", style_table_header), Paragraph("Detalhamento / Valor Unitário", style_table_header_right)],
        [Paragraph("Valor Base de Tabela (+ Frete se CIF)", style_table_text), Paragraph(format_currency((history_data.get('valor_tabela') or 0.0) + ((history_data.get('valor_frete') or 0.0) if history_data.get('frete_tipo') == 'CIF' else 0.0)), style_table_text_right)],
        [Paragraph("Frete (Informativo)", style_table_text), Paragraph(frete_str, style_table_text_right)],
        [Paragraph("Comissão do Representante", style_table_text), Paragraph(comissao_str, style_table_text_right)],
        [Paragraph("Subtotal com Comissão", style_table_text), Paragraph(format_currency(history_data.get('valor_com_comissao') or 0.0), style_table_text_right)],
        [Paragraph("Margem de Negociação Adicional", style_table_text), Paragraph(margem_str, style_table_text_right)],
        [Paragraph("Subtotal com Margem (Base DIFAL)", style_table_text), Paragraph(format_currency(history_data.get('valor_com_margem') or 0.0), style_table_text_right)],
        [Paragraph("Imposto DIFAL de Destino", style_table_text), Paragraph(difal_str, style_table_text_right)],
        [Paragraph("Valor Cheio da Venda (Preço Máximo)", style_table_text), Paragraph(format_currency(venda_cheio), style_table_text_right)],
        
        # Highlighted row (index 9)
        [Paragraph("Valor de Reserva (Mínimo Permitido)", style_table_text_warning), Paragraph(format_currency(minimo_venda), style_table_text_warning_right)],
        
        # New discount cap percent row (index 10)
        [Paragraph("Desconto Máximo Permitido", style_table_text_bold), Paragraph(format_percent(desconto_maximo_perc), style_table_text_right)],
        
        [Paragraph("Desconto Concedido", style_table_text), Paragraph(desconto_str, style_table_text_right)],
    ]
    
    pricing_table = Table(pricing_table_data, colWidths=[200, 160])
    pricing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_teal),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 0), (-1, 0), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2.5),
        ('TOPPADDING', (0, 1), (-1, -1), 2.5),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0, 7), (-1, 7), colors.HexColor('#F8FAFC')),
        
        # Soft red warning background for Valor de Reserva
        ('BACKGROUND', (0, 9), (-1, 9), colors.HexColor('#FEF2F2')),
        ('BOX', (0, 9), (-1, 9), 0.5, colors.HexColor('#FCA5A5')),
        
        # Zebra highlight for Desconto Máximo row
        ('BACKGROUND', (0, 10), (-1, 10), colors.HexColor('#F8FAFC')),
        
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#E2E8F0')),
    ]))
    
    right_flowables.append(pricing_table)
    right_flowables.append(Spacer(1, 8))
    
    # Highlighted Totals Card
    totals_data = [
        [
            Paragraph("VALOR UNITÁRIO FINAL", style_label),
            Paragraph("VALOR TOTAL FINAL PROPOSTA", style_label)
        ],
        [
            Paragraph(format_currency(history_data.get('valor_com_desconto') or 0.0), ParagraphStyle('ValUnit', fontName='Helvetica-Bold', fontSize=14, textColor=c_teal)),
            Paragraph(format_currency(history_data.get('venda_total') or 0.0), ParagraphStyle('ValTot', fontName='Helvetica-Bold', fontSize=16, textColor=c_azul_visuri))
        ]
    ]
    totals_table = Table(totals_data, colWidths=[180, 180])
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_badge_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_teal),
        ('LINEAFTER', (0, 0), (0, -1), 0.5, c_teal),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    right_flowables.append(totals_table)
    
    # ==========================================
    # 3. PARENT DASHBOARD TABLE LAYOUT
    # ==========================================
    # Printable area is 732 pt wide. Left col is 330, right col is 380, gap is 22.
    parent_table = Table([[left_flowables, "", right_flowables]], colWidths=[330, 22, 380])
    parent_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(parent_table)
    elements.append(Spacer(1, 10))
    
    # Legal Footer / Timestamp
    gerado_em = models.get_local_time().strftime("%d/%m/%Y %H:%M:%S")
    footer_text = f"Motor de Precificação Visuri &copy; {datetime.now().year} | Documento confidencial para uso interno corporativo. Gerado em: {gerado_em} BRT."
    elements.append(Paragraph(footer_text, style_footer_text))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
