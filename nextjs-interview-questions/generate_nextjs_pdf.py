import re
import os
from fpdf import FPDF

# Settings
BASE_DIR = r"c:\Users\sonyo\ChiragProject\nextjs-interview-questions"
README_PATH = os.path.join(BASE_DIR, "README.md")
PDF_PATH = os.path.join(BASE_DIR, "NextJS_Interview_Questions.pdf")
COVER_IMAGE = r"C:\Users\sonyo\.gemini\antigravity\brain\142a76b7-0f87-42d7-9b24-4b5f216491bd\nextjs_pdf_cover_1776725138078.png"

# Use fonts from the other project directory
FONT_DIR = r"c:\Users\sonyo\ChiragProject\100_Days_Of_Frontend_Interview_Questions"
FONTS = {
    "Roboto-Regular": os.path.join(FONT_DIR, "Roboto-Regular.ttf"),
    "Roboto-Bold": os.path.join(FONT_DIR, "Roboto-Bold.ttf"),
    "RobotoMono-Regular": os.path.join(FONT_DIR, "RobotoMono-Regular.ttf")
}

class NextJSPDF(FPDF):
    def __init__(self, use_custom_fonts=True):
        super().__init__()
        self.use_custom_fonts = use_custom_fonts
        self.font_reg = "Roboto-Regular" if use_custom_fonts else "Arial"
        self.font_bold = "Roboto-Bold" if use_custom_fonts else "Arial"
        self.font_mono = "RobotoMono-Regular" if use_custom_fonts else "Courier"

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(150)
            self.cell(0, 10, "Next.js Interview Questions & Answers", 0, 0, "R")
            self.ln(10)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font(self.font_reg, "", 8)
            self.set_text_color(150)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def clean_text(self, text):
        # Replace non-printable characters or characters that FPDF might struggle with
        # Also clean up markdown bold/italic tags that aren't handled by multi_cell
        text = text.replace("**", "").replace("_", "").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        # Remove navigation symbols
        text = text.replace("[:arrow_up: Back to Top](#groups)", "").replace("[:arrow_up: Back to Top](#common-table-of-contents)", "")
        if not self.use_custom_fonts:
            return "".join(i for i in text if ord(i) < 128)
        return text

    def chapter_title(self, label):
        self.ln(10)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 22)
        self.set_text_color(17, 17, 17) # Deep black
        self.cell(0, 20, self.clean_text(label), 0, 1, "L")
        self.ln(5)
        self.set_draw_color(0, 112, 243) # Next.js blue (accent)
        self.set_line_width(0.8)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(10)

    def question(self, num, text):
        self.ln(4)
        self.set_font(self.font_bold, "B" if not self.use_custom_fonts else "", 13)
        self.set_text_color(0, 0, 0)
        text = self.clean_text(text)
        self.multi_cell(0, 8, f"{num}. {text}", 0, "L")
        self.ln(2)

    def answer(self, text):
        self.set_font(self.font_reg, "", 10.5)
        self.set_text_color(60, 60, 60)
        text = text.replace("<br />", "\n").replace("\\", "")
        clean_ans = self.clean_text(text).strip()
        if clean_ans:
            self.multi_cell(0, 5.5, clean_ans, 0, "L")
            self.ln(3)

    def code_block(self, code):
        self.set_font(self.font_mono, "", 9)
        self.set_fill_color(248, 250, 252)
        self.set_text_color(30, 41, 59)
        code = self.clean_text(code)
        try:
            self.multi_cell(0, 5, code, 0, "L", fill=True)
        except:
            clean_code = "".join(i for i in code if ord(i) < 128)
            self.multi_cell(0, 5, clean_code, 0, "L", fill=True)
        self.ln(4)

def generate():
    # Verify fonts exist
    paths = FONTS
    use_custom = True
    for p in paths.values():
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            use_custom = False
            print(f"Font missing: {p}")
            break
            
    pdf = NextJSPDF(use_custom_fonts=use_custom)
    if use_custom:
        try:
            pdf.add_font("Roboto-Regular", "", paths["Roboto-Regular"])
            pdf.add_font("Roboto-Bold", "", paths["Roboto-Bold"])
            pdf.add_font("RobotoMono-Regular", "", paths["RobotoMono-Regular"])
        except Exception as e:
            print(f"Error loading fonts: {e}")
            pdf = NextJSPDF(use_custom_fonts=False)
    
    # --- COVER ---
    pdf.add_page()
    if os.path.exists(COVER_IMAGE):
        pdf.image(COVER_IMAGE, x=0, y=0, w=210, h=297)
    else:
        # Minimalist fallback if cover image failed
        pdf.set_fill_color(17, 17, 17)
        pdf.rect(0, 0, 210, 297, "F")
        pdf.set_y(100)
        pdf.set_font(pdf.font_bold, "B" if not pdf.use_custom_fonts else "", 36)
        pdf.set_text_color(255, 255, 255)
        pdf.multi_cell(0, 15, "NEXT.JS\nINTERVIEW\nQUESTIONS", 0, "C")
    
    # --- CONTENT ---
    if not os.path.exists(README_PATH):
        print(f"File not found: {README_PATH}")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split('\n')
    pdf.add_page()
    
    in_code_block = False
    code_buffer = []
    ignoring_toc = True # Start by ignoring the TOC at the beginning
    
    for line in lines:
        line_strip = line.strip()
        
        # Detect start of actual content (after TOC)
        if "### [Common]" in line_strip:
            ignoring_toc = False
            
        if ignoring_toc:
            continue
            
        # Ignore back-to-top links and separators
        if any(x in line_strip for x in ["Back to Top", "---", "### Table of Contents"]):
            continue
        
        if line_strip.startswith("### ["):
            # New Category
            cat_name = re.search(r"### \[(.*?)\]", line_strip)
            if cat_name:
                pdf.add_page()
                pdf.chapter_title(cat_name.group(1))
            continue
            
        # Match Question format: 1. ### What is NextJS?
        q_match = re.search(r"^(\d+)\.\s+###\s+(.*)", line_strip)
        if q_match:
            pdf.question(q_match.group(1), q_match.group(2))
            continue
            
        # Code Blocks
        if "```" in line_strip:
            if not in_code_block:
                in_code_block = True
                code_buffer = []
            else:
                in_code_block = False
                if code_buffer:
                    pdf.code_block("\n".join(code_buffer))
            continue
            
        if in_code_block:
            code_buffer.append(line)
            continue
            
        # Normal Answer Text
        if line_strip and not line_strip.startswith("|"): # Ignore tables for now as they are complex to render in FPDF
            pdf.answer(line_strip)

    pdf.output(PDF_PATH)
    print(f"PDF generated: {PDF_PATH}")

if __name__ == "__main__":
    generate()
