from fpdf import FPDF
from datetime import datetime, timedelta
import os

output_dir = "C:\\progetti\\git\\python\\1.0\\organizza_file\\input"
os.makedirs(output_dir, exist_ok=True)

now = datetime.now()

for i in range(1, 20):
    file_name = f"documento_{i:03}.pdf"
    path = os.path.join(output_dir, file_name)

    # Crea il PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"PDF di esempio numero {i}", ln=True)
    pdf.output(path)

    # Retrodata la modifica (1, 2, ..., 9 mesi fa)
    fake_time = now - timedelta(days=15 * i)
    mod_time = fake_time.timestamp()
    os.utime(path, (mod_time, mod_time))

print("PDF creati e datati correttamente.")