from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent


def main():
    pages = (BASE_DIR / "policy_source.txt").read_text(encoding="utf-8").split("\n---PAGE---\n")
    pdfmetrics.registerFont(UnicodeCIDFont("HYSMyeongJo-Medium"))
    c = canvas.Canvas(str(BASE_DIR / "policy.pdf")); c.setFont("HYSMyeongJo-Medium", 11)
    for page in pages:
        y = 800
        for line in page.splitlines(): c.drawString(50, y, line); y -= 22
        c.showPage(); c.setFont("HYSMyeongJo-Medium", 11)
    c.save(); print("policy.pdf generated")


if __name__ == "__main__": main()
