from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, grey
from reportlab.lib.units import mm
# Custom font ke liye ye imports zaroori hain
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_diary_page(filename):
    # --- Settings ---
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # --- FONT REGISTRATION ---
    # Yahan hum check kar rahe hain ki font file maujood hai ya nahi
    try:
        # 'Merienda.ttf' file aapke script wale folder mein honi chahiye
        pdfmetrics.registerFont(TTFont('Merienda', 'Merienda.ttf'))
        main_font = "Merienda"
        print("Merienda font successfully loaded!")
    except:
        print("Error: 'Merienda.ttf' file nahi mili! Default Helvetica use ho raha hai.")
        print("Please download Merienda font and rename it to 'Merienda.ttf'.")
        main_font = "Helvetica-Bold" # Fallback agar file na mile

    # Margins
    margin_left = 25 * mm
    margin_right = 15 * mm
    margin_top = 20 * mm
    margin_bottom = 15 * mm
    
    printable_width = width - margin_left - margin_right
    
    # --- 1. TITLE SECTION ---
    c.setFont(main_font, 24)
    c.setFillColor(black)
    c.drawCentredString(width / 2, height - margin_top - 10, "1 TO 1 MEETING")
    
    # --- 2. HEADER FIELDS ---
    y_cursor = height - margin_top - 50 
    
    c.setLineWidth(0.5)
    c.setStrokeColor(black)
    c.setFont(main_font, 9)
    
    # Helper to draw a field
    def draw_field(x, y, w, label):
        c.setFont(main_font, 8) # Using Merienda
        c.setFillColor(Color(0.4, 0.4, 0.4)) 
        c.drawString(x, y + 2, label)
        c.setStrokeColor(Color(0.7, 0.7, 0.7)) 
        c.line(x, y, x + w, y)
    
    # Row 1: SUBJECT | DATE
    col_gap = 10 * mm
    col_width = (printable_width - col_gap) / 2
    
    draw_field(margin_left, y_cursor, col_width, "SUBJECT:-")
    draw_field(margin_left + col_width + col_gap, y_cursor, col_width, "DATE:-")
    
    # Row 2: TIME | PLACE
    y_cursor -= 15 * mm
    draw_field(margin_left, y_cursor, col_width, "TIME:-")
    draw_field(margin_left + col_width + col_gap, y_cursor, col_width, "PLACE:-")
    
    # Row 3: MEETING WITH
    y_cursor -= 15 * mm
    draw_field(margin_left, y_cursor, printable_width, "MEETING WITH:-")
    
    # --- 3. SECTIONS & LINES ---
    line_height = 8 * mm 
    y_cursor -= 10 * mm 
    
    # Helper function to draw a section header
    def draw_section_header(y, title):
        header_height = 8 * mm
        
        # 1. Grey Background
        c.setFillColor(Color(0.92, 0.92, 0.92)) 
        c.rect(margin_left, y - header_height + 2, printable_width, header_height, fill=1, stroke=0)
        
        # 2. Centered Title Text
        c.setFont(main_font, 10) # Using Merienda
        c.setFillColor(Color(0.3, 0.3, 0.3)) 
        c.drawCentredString(width / 2, y - header_height + 4, title)
        
        return y - header_height

    # Helper function to draw lines
    def draw_ruling_lines(start_y, count):
        current_y = start_y
        c.setStrokeColor(Color(0.85, 0.85, 0.85)) 
        c.setLineWidth(0.5)
        
        for _ in range(count):
            current_y -= line_height
            c.line(margin_left, current_y, width - margin_right, current_y)
            
        return current_y

    # SECTION 1: DISCUSSION POINTS (8 Lines)
    y_cursor = draw_section_header(y_cursor, "DISCUSSION POINTS")
    y_cursor = draw_ruling_lines(y_cursor, 8)
    
    # SECTION 2: NOTES (14 Lines -> Changed to 10 as per your code)
    y_cursor -= 4 * mm 
    y_cursor = draw_section_header(y_cursor, "NOTES")
    y_cursor = draw_ruling_lines(y_cursor, 10)
    
    # SECTION 3: NEXT (8 Lines -> Changed to 4 as per your code)
    y_cursor -= 4 * mm 
    y_cursor = draw_section_header(y_cursor, "NEXT")
    y_cursor = draw_ruling_lines(y_cursor, 4)
    
    # --- Finalize ---
    c.showPage()
    c.save()
    print(f"PDF Generated successfully: {filename}")

if __name__ == "__main__":
    create_diary_page("1_on_1_Meeting_Diary_Merienda.pdf")