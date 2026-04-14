"""
Briefing Document Generator — H9CEAI CA12
Innovator Critique: From Pipeline to Position

Generates the submission PDF with Parts A-F.
Re-run this script each time a part is completed to rebuild the document.

Usage: python generate_briefing.py
"""

from fpdf import FPDF
import os
import textwrap

# === CONSTANTS ===
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Briefing_Document_24332780.pdf")

# Colours
NAVY = (0, 41, 82)
GOLD = (212, 168, 67)
DARK = (44, 44, 44)
MID_GREY = (100, 100, 100)
LIGHT_BG = (245, 240, 232)
WHITE = (255, 255, 255)
GREEN_ACCENT = (74, 124, 89)
AMBER_ACCENT = (232, 150, 12)
HUMAN_BG = (255, 248, 230)       # warm cream for human input sections
AI_BG = (240, 245, 250)          # cool blue-grey for AI-assisted sections
CRITICAL_BG = (255, 240, 240)    # soft red for critical thinking callouts


def safe(text):
    """Convert Unicode chars to Latin-1 safe equivalents for fpdf2."""
    if text is None:
        return ""
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--',
        '\u2026': '...', '\u2022': '*',
        '\u00a0': ' ', '\u2019': "'",
        '\u20ac': 'EUR',  # euro sign
        '\u2713': '[x]',  # checkmark
        '\u2717': '[ ]',  # cross
        '\u00b2': '2',    # superscript 2
        '\u00b3': '3',    # superscript 3
        '\u00a3': 'GBP',  # pound sign
        '\u2265': '>=',   # greater-equal
        '\u2264': '<=',   # less-equal
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')


class BriefingPDF(FPDF):
    """Custom PDF class for the H9CEAI briefing document."""

    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(25, 25, 25)

    def header(self):
        if self.page_no() == 1:
            return  # cover page has its own header
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5, safe("H9CEAI CA12 | Innovator Critique: From Pipeline to Position"), align="L")
        self.cell(0, 5, safe(f"Page {self.page_no()}"), align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(25, 13, self.w - 25, 13)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*MID_GREY)
        self.cell(0, 5, safe("Student ID: 24332780 | National College of Ireland"), align="C")

    # --- Layout helpers ---

    def cover_page(self):
        """Generate the cover page."""
        self.add_page()
        self.ln(40)

        # Title block
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(*NAVY)
        self.cell(0, 14, safe("Innovator Critique"), align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "", 16)
        self.set_text_color(*GOLD)
        self.cell(0, 10, safe("From Pipeline to Position"), align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(5)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        x_center = self.w / 2
        self.line(x_center - 40, self.get_y(), x_center + 40, self.get_y())
        self.ln(10)

        # Venture name
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*DARK)
        self.cell(0, 10, safe("HiveMap"), align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "I", 11)
        self.set_text_color(*MID_GREY)
        self.cell(0, 7, safe("See what the desert hides. Grow what the land remembers."), align="C", new_x="LMARGIN", new_y="NEXT")

        self.ln(20)

        # Metadata table
        meta = [
            ("Module", "Customer Engagement and Artificial Intelligence (H9CEAI)"),
            ("Programme", "MSc in AI for Business (MSCAIBUS1 / MSCAI)"),
            ("Lecturer", "Victor del Rosal"),
            ("Student ID", "24332780"),
            ("Date", "14 April 2026"),
            ("Repository", "github.com/SacriTom/24332780-innovator-critique"),
            ("GitHub Pages", "sacritom.github.io/24332780-innovator-critique/"),
            ("Pipeline Parameters", "Mauritania, Grapes, Bee, Flying, Haunted House"),
        ]

        self.set_font("Helvetica", "", 9)
        col_w = [50, 110]
        x0 = (self.w - sum(col_w)) / 2

        for label, value in meta:
            self.set_x(x0)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*NAVY)
            self.cell(col_w[0], 7, safe(label), border=0)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*DARK)
            self.cell(col_w[1], 7, safe(value), border=0, new_x="LMARGIN", new_y="NEXT")

        self.ln(15)

        # Contribution key
        self.set_x(x0)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*NAVY)
        self.cell(0, 7, safe("Contribution Key"), new_x="LMARGIN", new_y="NEXT")

        legend = [
            (HUMAN_BG, "HUMAN INPUT", "Author's original analysis, judgement, and critical thinking"),
            (AI_BG, "AI-ASSISTED", "Content generated or drafted with AI tools, reviewed by author"),
            (CRITICAL_BG, "CRITICAL THINKING", "Author's independent evaluation and reasoned position"),
        ]

        for bg, label, desc in legend:
            self.set_x(x0)
            self.set_fill_color(*bg)
            self.cell(8, 6, "", fill=True, border=1)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*DARK)
            self.cell(35, 6, safe(f"  {label}"))
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*MID_GREY)
            self.cell(0, 6, safe(f"  {desc}"), new_x="LMARGIN", new_y="NEXT")

    def part_heading(self, title):
        """Render a Part heading (e.g., 'Part A: Regulatory Audit...')."""
        if self.get_y() > 240:
            self.add_page()
        else:
            self.add_page()  # each part starts on a new page

        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 12, safe(f"  {title}"), fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_text_color(*DARK)

    def sub_heading(self, title):
        """Render a sub-heading within a part."""
        if self.get_y() > self.h - 40:
            self.add_page()
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.cell(0, 7, safe(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.3)
        self.line(25, self.get_y(), 90, self.get_y())
        self.ln(3)
        self.set_text_color(*DARK)

    def body_text(self, text, style="normal"):
        """Render body text. Style: normal, human, ai, critical."""
        bg_map = {
            "human": HUMAN_BG,
            "ai": AI_BG,
            "critical": CRITICAL_BG,
            "normal": None,
        }
        bg = bg_map.get(style)

        if bg:
            self.set_fill_color(*bg)
            # Tag label
            tag_labels = {"human": "[HUMAN INPUT]", "ai": "[AI-ASSISTED]", "critical": "[CRITICAL THINKING]"}
            tag_colors = {"human": AMBER_ACCENT, "ai": MID_GREY, "critical": (180, 50, 50)}
            self.set_font("Helvetica", "B", 7)
            self.set_text_color(*tag_colors.get(style, DARK))
            self.cell(0, 5, safe(tag_labels.get(style, "")), new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*DARK)

        if bg:
            x = self.l_margin + 2
            self.set_x(x)
            w = self.w - self.r_margin - x - 2
            # Draw background rect behind text
            y_start = self.get_y()
            # Dry run to measure height
            result = self.multi_cell(w, 5, safe(text), dry_run=True, output="LINES")
            n_lines = len(result) if result else 1
            block_h = n_lines * 5 + 4

            if self.get_y() + block_h > self.h - 25:
                self.add_page()
                y_start = self.get_y()

            self.set_fill_color(*bg)
            self.rect(self.l_margin, y_start - 1, self.w - self.l_margin - self.r_margin, block_h + 2, "F")
            self.set_xy(x, y_start)
            self.multi_cell(w, 5, safe(text))
            self.ln(3)
        else:
            self.set_font("Helvetica", "", 9)
            self.multi_cell(0, 5, safe(text))
            self.ln(2)

    def quoted_text(self, text, source=""):
        """Render a quoted block (for quoting from own files)."""
        self.set_fill_color(245, 245, 245)
        x = self.l_margin + 5
        self.set_x(x)
        w = self.w - self.r_margin - x - 5

        y_start = self.get_y()
        result = self.multi_cell(w, 5, safe(text), dry_run=True, output="LINES")
        n_lines = len(result) if result else 1
        block_h = n_lines * 5 + 4

        if self.get_y() + block_h > self.h - 25:
            self.add_page()
            y_start = self.get_y()

        # Grey background
        self.set_fill_color(245, 245, 245)
        self.rect(self.l_margin + 3, y_start - 1, self.w - self.l_margin - self.r_margin - 3, block_h + 2, "F")

        # Gold left bar
        self.set_fill_color(*GOLD)
        self.rect(self.l_margin + 3, y_start - 1, 2, block_h + 2, "F")

        self.set_font("Courier", "", 8)
        self.set_text_color(*DARK)
        self.set_xy(x, y_start)
        self.multi_cell(w, 5, safe(text))

        if source:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*MID_GREY)
            self.set_x(x)
            self.cell(w, 4, safe(f"-- {source}"))
            self.ln(2)

        self.ln(3)
        self.set_text_color(*DARK)

    def render_table(self, headers, rows, col_widths=None):
        """Render a table using the two-pass pattern from patterns.md."""
        if col_widths is None:
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / len(headers)] * len(headers)

        THICK, THIN, header_h = 0.5, 0.2, 8
        x0, y0 = self.get_x(), self.get_y()
        total_w = sum(col_widths)

        # Check for page break before header
        first_row_h = 8
        if self.get_y() + header_h + first_row_h > self.h - 25:
            self.add_page()
            x0, y0 = self.get_x(), self.get_y()

        # Header
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8)
        for i, h in enumerate(headers):
            cx = x0 + sum(col_widths[:i])
            self.rect(cx, y0, col_widths[i], header_h, "F")
            self.set_xy(cx, y0)
            self.cell(col_widths[i], header_h, safe(h), border=0, align="C")

        self.set_draw_color(*NAVY)
        self.set_line_width(THICK)
        self.rect(x0, y0, total_w, header_h)
        for i in range(1, len(headers)):
            vx = x0 + sum(col_widths[:i])
            self.line(vx, y0, vx, y0 + header_h)

        self.set_xy(x0, y0 + header_h)

        # Body rows
        self.set_draw_color(180, 180, 180)
        self.set_line_width(THIN)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*DARK)

        for row_idx, row in enumerate(rows):
            # Pass 1: measure
            row_h = 7
            for i, cell_text in enumerate(row):
                cell_w = col_widths[i] - 2
                if cell_w <= 0:
                    cell_w = 10
                result = self.multi_cell(cell_w, 4.5, safe(cell_text), border=0, dry_run=True, output="LINES")
                n_lines = len(result) if result else 1
                h = n_lines * 4.5 + 2
                row_h = max(row_h, h)

            if self.get_y() + row_h > self.h - 25:
                self.add_page()

            rx, ry = self.get_x(), self.get_y()

            # Alternating row background
            if row_idx % 2 == 0:
                self.set_fill_color(250, 250, 250)
            else:
                self.set_fill_color(*WHITE)
            self.rect(rx, ry, total_w, row_h, "F")

            # Pass 2: render
            for i, cell_text in enumerate(row):
                cx = rx + sum(col_widths[:i])
                self.set_xy(cx + 1, ry + 1)
                self.multi_cell(col_widths[i] - 2, 4.5, safe(cell_text), border=0)

            # Borders
            self.set_draw_color(180, 180, 180)
            self.set_line_width(THIN)
            self.line(rx, ry, rx + total_w, ry)
            self.line(rx, ry + row_h, rx + total_w, ry + row_h)
            self.line(rx, ry, rx, ry + row_h)
            self.line(rx + total_w, ry, rx + total_w, ry + row_h)
            for i in range(1, len(headers)):
                vx = rx + sum(col_widths[:i])
                self.line(vx, ry, vx, ry + row_h)

            self.set_xy(rx, ry + row_h)

        self.ln(4)

    def placeholder(self, text="[TO BE COMPLETED]"):
        """Render a placeholder marker for sections not yet written."""
        self.set_font("Helvetica", "BI", 10)
        self.set_text_color(180, 50, 50)
        self.cell(0, 8, safe(text), align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(*DARK)


# ============================================================
# CONTENT — Populate each part here as we complete them
# ============================================================

def build_part_a(pdf):
    """Part A: Regulatory Audit of Your Own Artefacts (25 marks)"""
    pdf.part_heading("Part A: Regulatory Audit of Your Own Artefacts (25 marks)")
    pdf.placeholder("[TO BE COMPLETED - Regulatory audit table + risk posture paragraph]")


def build_part_b(pdf):
    """Part B: Trust Transfer Audit (15 marks)"""
    pdf.part_heading("Part B: Trust Transfer Audit (15 marks)")
    pdf.placeholder("[TO BE COMPLETED - 3 trust-collapse moments with quotes]")


def build_part_c(pdf):
    """Part C: Conduct your own Research and Correct (15 marks)"""
    pdf.part_heading("Part C: Conduct your own Research and Correct (15 marks)")
    pdf.placeholder("[TO BE COMPLETED - Research verification report + corrections]")


def build_part_d(pdf):
    """Part D: Prototype (15 marks)"""
    pdf.part_heading("Part D: Prototype (15 marks)")
    pdf.placeholder("[TO BE COMPLETED - Prototype description + commit hash]")


def build_part_e(pdf):
    """Part E: Business modelling (15 marks)"""
    pdf.part_heading("Part E: Business modelling (15 marks)")
    pdf.placeholder("[TO BE COMPLETED - Ship decision in 250 words]")


def build_part_f(pdf):
    """Part F: The Plan (15 marks)"""
    pdf.part_heading("Part F: The Plan (15 marks)")
    pdf.placeholder("[TO BE COMPLETED - 90-day and 180-day plans with budget]")


def build_appendices(pdf):
    """Appendices — supporting evidence (does not count toward word budget)."""
    pdf.part_heading("Appendices")

    pdf.sub_heading("Appendix 1: Pipeline Parameters")
    pdf.body_text(
        "The AI Innovator pipeline was executed on 14 April 2026 with the following "
        "randomly assigned parameters: Country: Mauritania, Fruit: Grapes, Animal: Bee, "
        "Action: Flying, Wildcard: Haunted House. The pipeline generated 8 sequential "
        "outputs saved as separate files in the project repository.",
        style="ai"
    )

    pdf.sub_heading("Appendix 2: Repository & Submission Details")
    pdf.render_table(
        headers=["Item", "Value"],
        rows=[
            ["Public Repository", "github.com/SacriTom/24332780-innovator-critique"],
            ["GitHub Pages URL", "sacritom.github.io/24332780-innovator-critique/ai-innovator/projects/HiveMap/"],
            ["Initial Commit Hash", "3d911a7"],
            ["Pipeline Commit Hash", "0ee2f3d"],
            ["Final Commit Hash", "[TO BE RECORDED]"],
        ],
        col_widths=[45, 115]
    )

    pdf.sub_heading("Appendix 3: File Manifest")
    pdf.render_table(
        headers=["File", "Pipeline Step", "Description"],
        rows=[
            ["01-story.md", "Step (a)", "Short story weaving 5 parameters"],
            ["02-research-question.md", "Step (b)", "Academic research question"],
            ["03-problem-statement.md", "Step (c)", "Problem statement with customer segment"],
            ["04-solution-design.md", "Step (d)", "HiveMap solution design"],
            ["05-prototype.md", "Step (e)", "Prototype and design specifications"],
            ["index.html", "Step (f)", "Landing page"],
            ["pitch.html", "Step (g)", "Investor pitch deck (10 slides)"],
            ["07-business-plan.md", "Step (g)", "Business plan and marketing campaign"],
            ["prototype.html", "Part D", "Working alpha prototype"],
        ],
        col_widths=[45, 30, 85]
    )


# ============================================================
# MAIN — Build the full document
# ============================================================

def main():
    pdf = BriefingPDF()

    # Cover page
    pdf.cover_page()

    # Parts A-F
    build_part_a(pdf)
    build_part_b(pdf)
    build_part_c(pdf)
    build_part_d(pdf)
    build_part_e(pdf)
    build_part_f(pdf)

    # Appendices
    build_appendices(pdf)

    # Output
    pdf.output(OUTPUT_FILE)
    print(f"Briefing document generated: {OUTPUT_FILE}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    main()
