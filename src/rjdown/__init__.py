import argparse
import io
from typing import List

import httpx
from msgspec import Struct, convert, toml
from PIL import Image
from pypdf import PdfMerger


class BookStruct(Struct, kw_only=True, frozen=True):
    name: str
    id: str
    total_page: int


class CongfigStruct(Struct, kw_only=True, frozen=True):
    books: List[BookStruct]


def process_img(client: httpx.Client, id: str, page: int) -> io.BytesIO:
    img_byte = client.get(
        f"https://book.pep.com.cn/{id}/files/mobile/{page}.jpg"
    ).content
    img = Image.open(io.BytesIO(img_byte))
    pdf_byte = io.BytesIO()
    img.save(pdf_byte, format="pdf")
    pdf_byte.seek(0)
    return pdf_byte


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config file path")
    arge = parser.parse_args()
    with open(arge.config, "rb") as f:
        conf = convert(toml.decode(f.read()), CongfigStruct)

    client = httpx.Client()
    for book in conf.books:
        merger = PdfMerger()
        for i in range(1, book.total_page + 1):
            pdf_io = process_img(client, book.id, i)
            merger.append(pdf_io)
            print(f"{book.name} page {i} done")
        merger.write(f"output/{book.name}.pdf")
        merger.close()
