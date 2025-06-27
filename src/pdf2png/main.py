import os
from pathlib import Path
import fitz


INPUT_DIR = Path("/app/src/pdf2png/input")
OUTPUT_DIR = Path("/app/data/input")

class PdfToPng:
    def __init__(self, pdf_path: str, output_dir: str):
        self.pdf_path = pdf_path
        self.output_dir = output_dir

    def convert(self):
        pdf_files = list(INPUT_DIR.glob("*.pdf"))
        for pdf_file in pdf_files:
            try:
                doc = fitz.open(pdf_file)
                print(f"Processing: {pdf_file.name} ({doc.page_count} pages)")
                
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)

                    zoom = 2
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)

                    pdf_basename = pdf_file.stem
                    page_str = f"{page_num + 1:03d}"
                    output_filename = f"{pdf_basename}_{page_str}.png"
                    output_path = OUTPUT_DIR / output_filename

                    pix.save(output_path)
                    print(f"  - Saved: {output_path}")
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {e}")
            finally:
                doc.close()
        print("Conversion completed.")


if __name__ == "__main__":
    converter = PdfToPng(INPUT_DIR, OUTPUT_DIR)
    converter.convert()