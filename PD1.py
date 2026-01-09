from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_final_diary_page(filename):
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

    # --- 3. MARGINS ---
    margin_left = 25 * mm
    margin_right = 15 * mm
    margin_top = 20 * mm 
    printable_width = width - margin_left - margin_right
    
    # --- 4. HEADER FIELDS (TOP) ---
    y_cursor = height - margin_top - 10 
    
    c.setLineWidth(0.5)
    c.setStrokeColor(Color(0.5, 0.5, 0.5)) 
    
    def draw_field(x, y, w, label):
        c.setFont(main_font, 10) 
        c.setFillColor(Color(0.9, 0.9, 0.9)) 
        c.drawString(x, y + 2, label)
        c.setStrokeColor(Color(0.4, 0.4, 0.4)) 
        c.line(x, y, x + w, y)
    
    # Row 1
    col_gap = 10 * mm
    col_width = (printable_width - col_gap) / 2
    draw_field(margin_left, y_cursor, col_width, "Date:")
    draw_field(margin_left + col_width + col_gap, y_cursor, col_width, "Day:")
    
    # Row 2
    y_cursor -= 12 * mm
    draw_field(margin_left, y_cursor, col_width, "Mood:")
    draw_field(margin_left + col_width + col_gap, y_cursor, col_width, "Location:")
    
    # --- 5. FOOTER QUOTE (FIXED AT BOTTOM) ---
    # Isko hum sabse pehle fix kar dete hain taaki ye hile nahi
    footer_y_position = 12 * mm # Bottom edge se 12mm upar
    c.setFont(main_font, 9) # Thoda readable size
    c.setFillColor(Color(0.7, 0.7, 0.7)) # Light Grey
    c.drawCentredString(width / 2, footer_y_position, "“In the silence of the heart, God speaks.”")

    # --- 6. WRITING SECTIONS ---
    line_height = 7 * mm 
    y_cursor -= 15 * mm # Gap after header fields
    
    def draw_section_header(y, title):
        header_height = 8 * mm
        rect_bottom = y - header_height
        
        # Background Box
        c.setFillColor(Color(0.15, 0.15, 0.15)) 
        c.rect(margin_left, rect_bottom, printable_width, header_height, fill=1, stroke=0)
        
        # Centered Text
        c.setFont(main_font, 11) 
        c.setFillColor(white) 
        text_y_pos = rect_bottom + (header_height / 2) - 2.5 
        c.drawCentredString(width / 2, text_y_pos, title)
        
        return rect_bottom

    def draw_ruling_lines(start_y, count):
        current_y = start_y
        c.setStrokeColor(Color(0.3, 0.3, 0.3)) 
        c.setLineWidth(0.5)
        for _ in range(count):
            current_y -= line_height
            c.line(margin_left, current_y, width - margin_right, current_y)
        return current_y

    # --- CALCULATING SPACE ---
    # Humare paas "Tomorrow" ke liye 3 lines fix hain.
    # Humare paas "Gratitude" ke liye 4 lines standard hain.
    # Baaki bachi hui jagah hum "Story" ko denge.
    
    # SECTION 1: TODAY’S STORY (Maximum Space)
    # 22 lines rakhne se page nicely fill hoga bina footer ko touch kiye
    y_cursor = draw_section_header(y_cursor, "TODAY’S STORY")
    y_cursor = draw_ruling_lines(y_cursor, 22)
    
    # SECTION 2: GRATITUDE & THOUGHTS
    y_cursor -= 2 * mm 
    y_cursor = draw_section_header(y_cursor, "GRATITUDE & THOUGHTS")
    y_cursor = draw_ruling_lines(y_cursor, 4)
    
    # SECTION 3: TOMORROW'S FOCUS (Strictly 3 Lines)
    y_cursor -= 0 * mm 
    y_cursor = draw_section_header(y_cursor, "TOMORROW'S FOCUS")
    y_cursor = draw_ruling_lines(y_cursor, 3) 
    
    # Check: Ye last line footer ke upar honi chahiye.
    # Logic: 3 lines ke baad bhi niche kareeb 15-20mm jagah bachegi jahan footer quote akela hoga.

    # --- Finalize ---
    c.showPage()
    c.save()
    print(f"Final Diary Generated: {filename}")

if __name__ == "__main__":
    create_final_diary_page("PD1.pdf")