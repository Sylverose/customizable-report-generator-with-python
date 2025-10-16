"""Stamp the company logo on each page of an existing PDF report."""

import io
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# ANSI color codes
CYAN = '\033[96m'
RESET = '\033[0m'

# Paths
SRC_DIR = Path(__file__).parent
REPORT_PATH = (
    SRC_DIR.parent / 'reports' / 'product_purchases_report.pdf'
)
LOGO_PATH = SRC_DIR.parent / 'logo' / 'company_logo.png'
STAMPED_PATH = (
    SRC_DIR.parent / 'reports' / 'product_purchases_report_stamped.pdf'
)

# Settings for logo placement
LOGO_WIDTH = 60
LOGO_HEIGHT = 60
LOGO_X = 20
LOGO_Y = 750


def create_logo_overlay(page_width, page_height):
    """Create a PDF overlay with the logo at the top left corner."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    if LOGO_PATH.exists():
        logo = ImageReader(str(LOGO_PATH))
        x = 20
        y = page_height - LOGO_HEIGHT - 120
        
        # Draw white background behind logo
        can.setFillColorRGB(1, 1, 1)
        can.rect(x, y, LOGO_WIDTH, LOGO_HEIGHT, fill=1, stroke=0)
        can.drawImage(
            logo, x, y, width=LOGO_WIDTH, height=LOGO_HEIGHT, mask='auto'
        )
    can.save()
    packet.seek(0)
    return PdfReader(packet)


def stamp_logo_on_pdf():
    """Stamp logo on all pages of the PDF report."""
    reader = PdfReader(str(REPORT_PATH))
    writer = PdfWriter()
    page_width, page_height = A4[1], A4[0]
    overlay_pdf = create_logo_overlay(page_width, page_height)
    overlay_page = overlay_pdf.pages[0]
    for page in reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)
    with open(STAMPED_PATH, 'wb') as f:
        writer.write(f)
    print(f'{CYAN}The report has been stamped. Check the final result in '
          f'your "reports" folder{RESET}')


if __name__ == "__main__":
    stamp_logo_on_pdf()
