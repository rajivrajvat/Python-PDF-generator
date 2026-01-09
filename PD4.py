from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_diary_pd4(filename):
    # --- Settings ---
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # --- 1. LOAD FONT ---
    try:
        # 'Merienda.ttf' file script ke saath honi chahiye
        pdfmetrics.registerFont(TTFont('Merienda', 'Merienda.ttf'))
        main_font = "Merienda"
        print("Merienda font loaded successfully!")
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
    
    # --- 4. START POSITION (Headers Removed) ---
    # Date/Day/Mood hata diya hai, isliye cursor upar se start hoga
    y_cursor = height - margin_top - 5 
    
    # --- 5. FOOTER QUOTE (Fixed at Bottom) ---
    footer_y_position = 12 * mm 
    c.setFont(main_font, 9) 
    c.setFillColor(Color(0.7, 0.7, 0.7)) # Light Grey
    # New Quote added here
    c.drawCentredString(width / 2, footer_y_position, "“Stop acting so small. You are the universe in ecstatic motion.” — Rumi")

    # --- 6. WRITING SECTIONS ---
    line_height = 7 * mm 
    
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

    # --- SECTIONS ---
    
    # SECTION 1: TODAY’S STORY 
    # Header hatne se jagah bachi thi, isliye lines 22 se badhakar 26 kar di hain
    y_cursor = draw_section_header(y_cursor, "REST STORY")
    y_cursor = draw_ruling_lines(y_cursor, 26)
    
    # SECTION 2: GRATITUDE & THOUGHTS
    y_cursor -= 2 * mm # Thoda gap
    y_cursor = draw_section_header(y_cursor, "GRATITUDE & THOUGHTS")
    y_cursor = draw_ruling_lines(y_cursor, 4)
    
    # SECTION 3: TOMORROW'S FOCUS (Strictly 3 Lines)
    y_cursor -= 2 * mm # Thoda gap
    y_cursor = draw_section_header(y_cursor, "TOMORROW'S FOCUS")
    y_cursor = draw_ruling_lines(y_cursor, 3) 
    
    # --- Finalize ---
    c.showPage()
    c.save()
    print(f"Final Diary Generated: {filename}")

if __name__ == "__main__":
    create_diary_pd4("PD4.pdf")