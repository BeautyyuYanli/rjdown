import argparse
import io
from typing import List, Dict, Optional
from time import sleep

import httpx
from msgspec import Struct, convert, toml, field
from PIL import Image
from pypdf import PdfMerger


class BookStruct(Struct, kw_only=True, frozen=True):
    name: str
    id: str
    total_page: int


class CongfigStruct(Struct, kw_only=True, frozen=True):
    request_per_second: Optional[float] = None
    books: List[BookStruct]
    request_header: Dict[str, str] = field(default_factory=dict)


def process_img(client: httpx.Client, id: str, page: int) -> io.BytesIO:
    img_byte = client.get(
        f"https://book.pep.com.cn/{id}/files/mobile/{page}.jpg",
        headers={
            **client.headers,
            "Referer": f"https://book.pep.com.cn/{id}/mobile/index.html",
        },
    ).content

    if img_byte == b"":  # 处理空白页
        img = Image.new("RGB", (1274, 1800), (255, 255, 255))
        print("第" + page + "页为空白！")
    else:
        try:
            img = Image.open(io.BytesIO(img_byte))  # 检查返回的内容是否是图片格式
        except:
            print("出错了，响应结果为：")
            print(img_byte)
            exit()

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

    client = httpx.Client(headers=conf.request_header)
    for book in conf.books:
        merger = PdfMerger()
        for i in range(1, book.total_page + 1):
            pdf_io = process_img(client, book.id, i)
            merger.append(pdf_io)
            print(f"{book.name} page {i} done")
            if conf.request_per_second:
                sleep(1 / conf.request_per_second)
        merger.write(f"output/{book.name}.pdf")
        merger.close()
