import os
import re
from fpdf import FPDF

# Settings
BASE_DIR = r"c:\Users\sonyo\ChiragProject"
TEXT_PATH = os.path.join(BASE_DIR, "System_Design.txt")
PDF_PATH = os.path.join(BASE_DIR, "System_Design_Interview_Guide.pdf")

# Images from the session
COVER_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\sysdesign_cover_1776725552773.png"
LB_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\load_balancer_diagram_1776725569192.png"
MICROSERVICES_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\microservices_diagram_1776725587139.png"
SHARDING_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\database_sharding_diagram_1776725603179.png"

# Use fonts from the other project directory
FONT_DIR = r"c:\Users\sonyo\ChiragProject\100_Days_Of_Frontend_Interview_Questions"
FONTS = {
    "Roboto-Regular": os.path.join(FONT_DIR, "Roboto-Regular.ttf"),
    "Roboto-Bold": os.path.join(FONT_DIR, "Roboto-Bold.ttf"),
}

class SystemDesignPDF(FPDF):
    def __init__(self, use_custom_fonts=True):
        super().__init__()
        self.use_custom_fonts = use_custom_fonts
        self.font_reg = "Roboto-Regular" if use_custom_fonts else "Arial"
        self.font_bold = "Roboto-Bold" if use_custom_fonts else "Arial"

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(150)
            self.cell(0, 10, "System Design Interview Guide", 0, 0, "R")
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(150)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def section_header(self, text):
        self.ln(10)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 20)
        self.set_text_color(0, 128, 128) # Teal
        self.cell(0, 15, text, 0, 1, "L")
        self.set_draw_color(0, 128, 128)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(8)

    def sub_header(self, text):
        self.ln(5)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, text, 0, 1, "L")
        self.ln(2)

    def item_point(self, text, indent=0):
        self.set_font(self.font_reg, "", 10.5)
        self.set_text_color(60, 60, 60)
        prefix = "• " if indent == 0 else "  - "
        self.set_x(self.get_x() + (indent * 5))
        self.multi_cell(0, 6, f"{prefix}{text}", 0, "L")
        self.ln(1)

    def add_diagram(self, img_path, caption):
        if os.path.exists(img_path):
            self.ln(5)
            # Try to center image
            self.image(img_path, x=25, w=160)
            self.ln(2)
            self.set_font(self.font_reg, "", 9)
            self.set_text_color(100)
            self.cell(0, 10, f"Diagram: {caption}", 0, 1, "C")
            self.ln(5)

def generate():
    use_custom = True
    for p in FONTS.values():
        if not os.path.exists(p):
            use_custom = False
            break
            
    pdf = SystemDesignPDF(use_custom_fonts=use_custom)
    if use_custom:
        pdf.add_font("Roboto-Regular", "", FONTS["Roboto-Regular"])
        pdf.add_font("Roboto-Bold", "", FONTS["Roboto-Bold"])
    
    # --- COVER ---
    pdf.add_page()
    if os.path.exists(COVER_IMAGE):
        pdf.image(COVER_IMAGE, x=0, y=0, w=210, h=297)
    
    # --- CONTENT ---
    if not os.path.exists(TEXT_PATH):
        print("Text file not found!")
        return

    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pdf.add_page()
    
    top_sections = [
        "General Software Development", "Backend Development", "Frontend Development",
        "Full-Stack Development", "MERN Stack Development", "Cross-Cutting Concerns",
        "Interview Tips for System Design", "Quick Reference: Architecture Patterns"
    ]
    
    sub_sections = [
        "Fundamentals", "Intermediate", "API & Service Design", "Database Design",
        "Real-time Systems", "Performance & Architecture", "Optimization",
        "End-to-End Systems", "Integration & Workflow", "React Specific",
        "Express.js Specific", "MongoDB Specific", "MERN Integration",
        "Scalability & Performance", "Reliability & Fault Tolerance", "Security",
        "Monitoring & Observability", "Approach", "Key Metrics to Discuss",
        "Common Technologies to Know"
    ]

    for line in lines:
        line_strip = line.strip()
        if not line_strip or line_strip == "Table of Contents":
            continue
            
        if line_strip in top_sections:
            pdf.add_page()
            pdf.section_header(line_strip)
            
            # Contextual Images
            if "Backend Development" in line_strip:
                pdf.add_diagram(MICROSERVICES_IMAGE, "Microservices Architecture")
            if "General Software Development" in line_strip:
                pdf.add_diagram(LB_IMAGE, "Load Balancing distribution")
            if "Cross-Cutting Concerns" in line_strip:
                pdf.add_diagram(SHARDING_IMAGE, "Database Sharding & Scalability")
            continue
            
        if line_strip in sub_sections:
            pdf.sub_header(line_strip)
            continue
            
        # Distinguish between questions and details
        if "?" in line_strip or line_strip.startswith("Design"):
            pdf.item_point(line_strip, indent=0)
        else:
            pdf.item_point(line_strip, indent=1)

    pdf.output(PDF_PATH)
    print(f"PDF generated: {PDF_PATH}")

if __name__ == "__main__":
    generate()
