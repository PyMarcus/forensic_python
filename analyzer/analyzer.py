import os
import typing
from typing import Tuple, Any

import PyPDF2
import argparse
import aiofiles
import asyncio


class Analyzer:
    def __init__(self, pdf_path: str, author: str) -> None:
        self.__pdf_path: str = "{0}".format(pdf_path)
        self._author: str = author

    @staticmethod
    def get_pdf_path() -> tuple[Any, Any]:
        parse = argparse.ArgumentParser(description="Recover metadata from pdf")
        parse.add_argument("-f", "--file", required=True, type=str)
        parse.add_argument("-a", "--author", required=True, type=str)
        args = parse.parse_args()
        if os.path.isdir(args.file):
            return args.file, args.author
        raise FileNotFoundError("Directory not exists")

    async def __recover_metadata(self) -> typing.List[typing.Dict[typing.Any,
                                                                  typing.Any]]:
        metadata: typing.List[typing.Any] = list()
        for file in os.listdir(self.__pdf_path):
            try:
                reader = PyPDF2.PdfReader(os.path.join(self.__pdf_path, file))
                metadata.append({os.path.join(os.path.abspath(self.__pdf_path), file): reader.metadata})
            except PermissionError:
                ...
        return metadata

    async def __write_in_file(self) -> None:
        metadata: typing.List[typing.Dict[typing.Any, typing.Any]]\
            = await self.__recover_metadata()
        counter: int = 0
        async with aiofiles.open("result.txt", "w", encoding="latin1") as f:
            await f.writelines(f"Author: {self._author}\n")
            for meta in metadata:
                for k, v in meta.items():
                    if v.get("/Author") == self._author:
                        await f.writelines(f"Founded in: {k}\n")
                        counter = 1
            if not counter:
                await f.writelines(f"Not found\n")

    def start(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__write_in_file())
