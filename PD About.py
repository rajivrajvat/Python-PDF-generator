from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_intro_page_v3(filename):
    # --- Settings ---
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # --- 1. LOAD FONT ---
    try:
        pdfmetrics.registerFont(TTFont('Merienda', 'Merienda.ttf'))
        main_font = "Merienda"
    except:
        main_font = "Helvetica-Bold"
        print("Merienda font not found. Using Helvetica.")

    # --- 2. BLACK BACKGROUND ---
    c.setFillColor(black)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # --- 3. LAYOUT CONSTANTS ---
    margin_left = 25 * mm
    margin_right = 15 * mm
    margin_top = 15 * mm 
    printable_width = width - margin_left - margin_right
    
    # Row Spacing Settings (Slightly compact to Create Gap at Bottom)
    row_height = 9 * mm   # Pehle 10mm tha, ab 9mm kiya
    section_gap = 3 * mm  # Pehle 4mm tha, ab 3mm kiya
    
    # --- 4. DRAW HEADER (TITLE) ---
    c.setFont(main_font, 22)
    c.setFillColor(white)
    c.drawCentredString(width / 2, height - margin_top - 10, "THIS DIARY BELONGS TO")
    
    # Cursor start point
    y_cursor = height - margin_top - 25 * mm

    # --- HELPER FUNCTIONS ---
    
    def draw_section_header(y, title):
        header_h = 7 * mm
        rect_bottom = y - header_h
        
        # Dark Grey Background for Header
        c.setFillColor(Color(0.15, 0.15, 0.15)) 
        c.rect(margin_left, rect_bottom, printable_width, header_h, fill=1, stroke=0)
        
        # Centered Text
        c.setFont(main_font, 10) 
        c.setFillColor(white) 
        c.drawCentredString(width / 2, rect_bottom + 2 * mm, title)
        
        # Return new cursor position
        return rect_bottom - 8 * mm

    def draw_field(x, y, w, label):
        # Label
        c.setFont(main_font, 9) 
        c.setFillColor(Color(0.8, 0.8, 0.8)) # Light Grey
        c.drawString(x, y + 2, label)
        
        # Line
        c.setStrokeColor(Color(0.4, 0.4, 0.4)) 
        c.setLineWidth(0.5)
        c.line(x, y, x + w, y)

    # --- 5. DRAW CONTENT SECTIONS ---

    col_gap = 10 * mm
    half_width = (printable_width - col_gap) / 2

    # --- SECTION 1: IDENTITY ---
    y_cursor = draw_section_header(y_cursor, "BASIC IDENTITY")
    
    draw_field(margin_left, y_cursor, printable_width, "Full Name:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, half_width, "Nickname:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Date of Birth:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, half_width, "Blood Group:")
    y_cursor -= (row_height + section_gap)

    # --- SECTION 2: CONTACT ---
    y_cursor = draw_section_header(y_cursor, "CONTACT DETAILS")
    
    draw_field(margin_left, y_cursor, half_width, "Mobile Number:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Alt. Mobile:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, printable_width, "Email Address:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, printable_width, "Home Address:")
    y_cursor -= (row_height + section_gap)

    # --- SECTION 3: PROFESSIONAL ---
    y_cursor = draw_section_header(y_cursor, "PROFESSIONAL INFO")
    
    draw_field(margin_left, y_cursor, half_width, "Job Title:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Company:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, printable_width, "Office Address / Work Email:")
    y_cursor -= (row_height + section_gap)

    # --- SECTION 4: FAMILY ---
    y_cursor = draw_section_header(y_cursor, "FAMILY DETAILS")
    
    draw_field(margin_left, y_cursor, half_width, "Father's Name:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Mother's Name:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, half_width, "Spouse Name:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Children:")
    y_cursor -= (row_height + section_gap)

    # --- SECTION 5: PERSONAL ---
    y_cursor = draw_section_header(y_cursor, "PERSONAL CORNER")
    
    draw_field(margin_left, y_cursor, printable_width, "Hobbies / Interests:")
    y_cursor -= row_height
    
    draw_field(margin_left, y_cursor, printable_width, "Favorite Quote / Values:")
    y_cursor -= (row_height + section_gap)

    # --- SECTION 6: EMERGENCY (Fixed Spacing) ---
    y_cursor = draw_section_header(y_cursor, "EMERGENCY CONTACT")
    
    draw_field(margin_left, y_cursor, half_width, "Contact Name:")
    draw_field(margin_left + half_width + col_gap, y_cursor, half_width, "Mobile No:")
    
    # --- 6. FOOTER (FIXED & CLEAN) ---
    
    # Calculation:
    # Divider Line ko ab hum 32mm par rakhenge (Pehle 40mm par thi, jo overlap kar rahi thi)
    # Emergency fields ab kareeb 55-60mm height par khatam honge.
    # Gap almost 20-25mm ka hoga. No overlap possible.

    divider_y = 32 * mm 
    
    # 1. Divider Line
    c.setStrokeColor(Color(0.5, 0.5, 0.5))
    c.setLineWidth(1)
    c.line(margin_left, divider_y, width - margin_right, divider_y)
    
    # 2. "If Found" Text
    text_y = divider_y - 8 * mm
    c.setFont(main_font, 12)
    c.setFillColor(white)
    c.drawCentredString(width / 2, text_y, "IF FOUND, PLEASE CONTACT:")
    
    # 3. Big Number Field
    number_y = text_y - 10 * mm
    c.setFont(main_font, 14)
    c.setFillColor(Color(0.8, 0.8, 0.8))
    
    # Drawing Number Line cleanly
    prefix = "+91 "
    prefix_width = c.stringWidth(prefix, main_font, 14)
    line_len = 80 * mm
    total_w = prefix_width + line_len
    start_x = (width - total_w) / 2
    
    c.drawString(start_x, number_y, prefix)
    
    c.setStrokeColor(Color(0.6, 0.6, 0.6))
    c.setLineWidth(1)
    c.line(start_x + prefix_width, number_y - 1, start_x + total_w, number_y - 1)

    # --- Finalize ---
    c.showPage()
    c.save()
    print(f"Intro Page Fixed V3: {filename}")

if __name__ == "__main__":
    create_intro_page_v3("PD_About.pdf")