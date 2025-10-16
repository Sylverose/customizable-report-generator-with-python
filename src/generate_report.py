"""Generate PDF report of product purchases using pandas."""

from datetime import datetime
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from connect import config, logger, mysql_connection

# ANSI color codes
CYAN = '\033[96m'
RESET = '\033[0m'

# Define the reports directory path
REPORTS_DIR = Path(__file__).parent.parent / 'reports'

# Load custom font
FONT_PATH = (
    Path(__file__).parent.parent / 'fonts' / 'playfair-display.italic.ttf'
)
custom_font = fm.FontProperties(fname=str(FONT_PATH))


def generate_purchase_report():
    """Generate a PDF report of product purchases joined from orders and products tables."""
    try:
        REPORTS_DIR.mkdir(exist_ok=True)
        
        query = """
            SELECT p.product_name, o.date_time, p.price
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            ORDER BY o.date_time DESC
        """
        
        with mysql_connection(config) as conn:
            if conn is not None:
                df = pd.read_sql(query, conn)
                
                if df.empty:
                    logger.warning("No data found for report generation")
                    return False
                
                # Format datetime and price columns
                df['date_time'] = pd.to_datetime(
                    df['date_time']
                ).dt.strftime('%Y-%m-%d %H:%M:%S')
                df['price'] = df['price'].map(lambda x: f"{x:.2f}")
                
                # Rename columns
                df.columns = [
                    'Product Name',
                    'Purchase Date & Time',
                    'Price in DKK'
                ]
                
                # Create PDF with pagination
                pdf_path = REPORTS_DIR / 'product_purchases_report.pdf'
                
                # Calculate rows per page based on A4 landscape dimensions
                row_height = 0.045
                table_top_margin = 0.165
                table_bottom_margin = 0.05
                available_height = 1 - table_top_margin - table_bottom_margin
                max_rows_per_page = int(available_height / row_height) - 1
                rows_per_page = max_rows_per_page
                num_pages = (len(df) + rows_per_page - 1) // rows_per_page
                with PdfPages(str(pdf_path)) as pdf:
                    for page in range(num_pages):
                        start = page * rows_per_page
                        end = min(start + rows_per_page, len(df))
                        df_chunk = df.iloc[start:end]

                        fig, ax = plt.subplots(figsize=(11.69, 8.27))
                        ax.axis('tight')
                        ax.axis('off')

                        nrows = len(df_chunk) + 1  # +1 for header
                        table_height = row_height * nrows
                        table = ax.table(
                            cellText=df_chunk.values,
                            colLabels=df.columns,
                            cellLoc='left',
                            loc='center',
                            colWidths=[0.4, 0.4, 0.2],
                            bbox=[
                                0,
                                1 - table_top_margin - table_height,
                                1,
                                table_height
                            ]
                        )

                        # Right-align price column
                        price_col_idx = 2
                        for row in range(len(df_chunk) + 1):
                            table[(row, price_col_idx)].set_text_props(ha='right')

                        # Apply table styling
                        table.auto_set_font_size(False)
                        table.set_fontsize(9)
                        table.scale(1, 1.5)

                        # Style header row
                        for i in range(len(df.columns)):
                            table[(0, i)].set_facecolor('#3A1772')
                            table[(0, i)].set_text_props(
                                weight='bold', color='white', ha='left'
                            )

                        # Apply alternate row colors
                        for i in range(1, len(df_chunk) + 1):
                            if i % 2 == 0:
                                for j in range(len(df.columns)):
                                    table[(i, j)].set_facecolor('#ffe6f0')

                        # Add report title
                        plt.text(
                            0.5, 1.01 - 0.059, 'Total purchases report',
                            fontsize=20, weight='bold', ha='center',
                            va='bottom', transform=ax.transAxes,
                            fontproperties=custom_font, color='#D741A7'
                        )
                        
                        # Add report date
                        current_date = datetime.now().strftime(
                            'Report date: %Y-%m-%d'
                        )
                        plt.text(
                            1, 1.01, current_date, fontsize=10,
                            ha='right', va='bottom',
                            transform=ax.transAxes, color='#3A1772'
                        )
                        pdf.savefig(fig, bbox_inches='tight')
                        plt.close()
                
                logger.info(f"PDF report generated successfully at {pdf_path}")
                print(f"\n{CYAN}The report has been generated. You can now run "
                      f"python src\\stamp_logo_on_pdf.py to add your company "
                      f"logo or watermark to your report.{RESET}")
                print(f"Total records: {len(df)}")
                return True
            else:
                logger.error("Failed to establish database connection")
                return False
                
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return False


if __name__ == "__main__":
    generate_purchase_report()
