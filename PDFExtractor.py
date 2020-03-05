import subprocess


class PDFExtractor:
    @classmethod
    def read(cls, pdfpath):
        cp = subprocess.run(["pdftotext", f"{pdfpath}", "-"], stdout=subprocess.PIPE)
        return cp.stdout.decode('utf8')