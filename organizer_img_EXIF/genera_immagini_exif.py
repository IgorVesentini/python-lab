import os
import argparse
import random
from datetime import datetime, timedelta
from PIL import Image
import piexif

def genera_exif_variabili(index, base_time):
    exif_date = base_time + timedelta(days=index, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    exif_str = exif_date.strftime("%Y:%m:%d %H:%M:%S")

    marche = ["Canon", "Nikon", "Sony", "Fujifilm", "Pentax"]
    modelli = ["A100", "X-T3", "Z5", "EOS 2000D", "Coolpix"]
    software = ["PythonScript", "ImgGen", "MetaCreator", "PhotoBot"]
    obiettivi = ["Sigma", "Tamron", "Zeiss", "Canon Lens", "Nikkor"]

    iso = random.choice([100, 200, 400, 800, 1600])
    esposizione = (1, random.choice([60, 125, 250, 500]))
    apertura = random.choice([1.8, 2.8, 4.0, 5.6])

    zeroth_ifd = {
        piexif.ImageIFD.Make: random.choice(marche),
        piexif.ImageIFD.Model: random.choice(modelli),
        piexif.ImageIFD.Software: random.choice(software),
    }

    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: exif_str,
        piexif.ExifIFD.LensMake: random.choice(obiettivi),
        piexif.ExifIFD.ISOSpeedRatings: iso,
        piexif.ExifIFD.ExposureTime: esposizione,
        piexif.ExifIFD.FNumber: (int(apertura * 10), 10),  # ad esempio (28, 10) → f/2.8
    }

    return {"0th": zeroth_ifd, "Exif": exif_ifd}

def crea_immagini(n, output_dir="test_img"):
    os.makedirs(output_dir, exist_ok=True)
    base_time = datetime(2022, 1, 1, 12, 0, 0)

    for i in range(n):
        img = Image.new("RGB", (200, 200), (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))

        exif_dict = genera_exif_variabili(i, base_time)
        exif_bytes = piexif.dump(exif_dict)

        filename = os.path.join(output_dir, f"img_{i+1:02}.jpg")
        img.save(filename, "jpeg", exif=exif_bytes)

    print(f"✅ {n} immagini create in '{output_dir}' con EXIF *diversi* su più campi.")

def main():
    parser = argparse.ArgumentParser(description="Genera immagini JPG con EXIF diversi.")
    parser.add_argument("--numero", type=int, required=True, help="Numero di immagini da generare")
    args = parser.parse_args()
    crea_immagini(args.numero)

if __name__ == "__main__":
    main()
