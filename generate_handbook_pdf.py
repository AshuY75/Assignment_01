import os
import re
from fpdf import FPDF

# Settings
BASE_DIR = r"c:\Users\sonyo\ChiragProject"
MD_PATH = os.path.join(BASE_DIR, "System_Design_Handbook_Part1.md")
PDF_PATH = os.path.join(BASE_DIR, "System_Design_Interview_Handbook.pdf")

# Images from the session
COVER_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\handbook_cover_v2_1776726265258.png"
CAP_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\cap_theorem_diagram_1776726282289.png"
GATEWAY_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\api_gateway_diagram_v2_1776726302787.png"
CDN_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\cdn_mechanics_v2_1776726362792.png"
SHARDING_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\db_sharding_premium_1776726381213.png"

# Use fonts from the other project directory
FONT_DIR = r"c:\Users\sonyo\ChiragProject\100_Days_Of_Frontend_Interview_Questions"
FONTS = {
    "Roboto-Regular": os.path.join(FONT_DIR, "Roboto-Regular.ttf"),
    "Roboto-Bold": os.path.join(FONT_DIR, "Roboto-Bold.ttf"),
    "RobotoMono-Regular": os.path.join(FONT_DIR, "RobotoMono-Regular.ttf"),
}

class HandbookPDF(FPDF):
    def __init__(self, use_custom_fonts=True):
        super().__init__()
        self.use_custom_fonts = use_custom_fonts
        self.font_reg = "Roboto-Regular" if use_custom_fonts else "Arial"
        self.font_bold = "Roboto-Bold" if use_custom_fonts else "Arial"
        self.font_mono = "RobotoMono-Regular" if use_custom_fonts else "Courier"

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(120)
            self.cell(0, 10, "The Ultimate System Design Interview Handbook", 0, 0, "R")
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(150)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def h1(self, text):
        self.ln(10)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 28)
        self.set_text_color(10, 20, 60) # Deep Navy
        self.cell(0, 20, text, 0, 1, "L")
        self.set_draw_color(0, 120, 212) # Modern Blue
        self.set_line_width(1)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(12)

    def h2(self, text):
        self.ln(8)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 20)
        self.set_text_color(0, 112, 243) # Next Blue
        self.cell(0, 15, text, 0, 1, "L")
        self.ln(5)

    def h3(self, text):
        self.ln(5)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 12, text, 0, 1, "L")
        self.ln(2)

    def body_text(self, text):
        self.set_font(self.font_reg, "", 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, text, 0, "L")
        self.ln(4)

    def list_item(self, text, indent=1):
        self.set_font(self.font_reg, "", 11)
        self.set_text_color(60, 60, 60)
        prefix = "• " if indent == 1 else "  - "
        self.set_x(self.get_x() + (indent * 5))
        self.multi_cell(0, 6, f"{prefix}{text}", 0, "L")
        self.ln(1)

    def code_block(self, code):
        self.set_font(self.font_mono, "", 9)
        self.set_fill_color(245, 247, 250)
        self.set_text_color(30, 40, 50)
        self.multi_cell(0, 5, code, 0, "L", fill=True)
        self.ln(4)

    def add_diagram(self, img_path, caption):
        if os.path.exists(img_path):
            self.ln(5)
            self.image(img_path, x=25, w=160)
            self.ln(2)
            self.set_font(self.font_reg, "", 9)
            self.set_text_color(100)
            self.cell(0, 10, f"Architecture Figure: {caption}", 0, 1, "C")
            self.ln(5)

def generate():
    use_custom = True
    for p in FONTS.values():
        if not os.path.exists(p):
            use_custom = False
            break
            
    pdf = HandbookPDF(use_custom_fonts=use_custom)
    if use_custom:
        pdf.add_font("Roboto-Regular", "", FONTS["Roboto-Regular"])
        pdf.add_font("Roboto-Bold", "", FONTS["Roboto-Bold"])
        pdf.add_font("RobotoMono-Regular", "", FONTS["RobotoMono-Regular"])
    
    # --- COVER ---
    pdf.add_page()
    if os.path.exists(COVER_IMAGE):
        pdf.image(COVER_IMAGE, x=0, y=0, w=210, h=297)

    # --- PART 1 ---
    if not os.path.exists(MD_PATH):
        print("MD file not found!")
        return

    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line_strip = line.strip()
        if not line_strip: continue
        
        if line_strip.startswith("# "):
            pdf.add_page()
            pdf.h1(line_strip[2:])
        elif line_strip.startswith("## "):
            pdf.h2(line_strip[3:])
            
            # Contextual Images
            if "Core Concepts" in line_strip:
                pdf.add_diagram(CAP_IMAGE, "The CAP Theorem Trade-offs")
            if "API Fundamentals" in line_strip:
                pdf.add_diagram(GATEWAY_IMAGE, "Centralized API Gateway Pattern")
            if "Database Fundamentals" in line_strip:
                pdf.add_diagram(SHARDING_IMAGE, "Horizontal Database Sharding")
            if "Caching Fundamentals" in line_strip:
                pdf.add_diagram(CDN_IMAGE, "Global Content Delivery Network (CDN)")
                
        elif line_strip.startswith("### "):
            pdf.h3(line_strip[4:])
        elif line_strip.startswith("- "):
            pdf.list_item(line_strip[2:])
        else:
            pdf.body_text(line_strip)

    pdf.output(PDF_PATH)
    print(f"PDF generated: {PDF_PATH}")

if __name__ == "__main__":
    generate()
