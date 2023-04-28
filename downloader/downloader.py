import os

import aiohttp
import aiofiles
import asyncio
import typing
from termcolor import colored, cprint


class Downloader:
    """
    Baixa, por padrão, o pdf de 10 sites pré-estabelecidos
    Do contrário, baixa dos sites especificados na lista do método
    inicializador __init__
    """
    def __init__(self, download_list: typing.Optional[typing.List[str]] = None,
                 destination: typing.Optional[str] = "pdfs") -> None:
        if download_list is not None:
            self.__download_list: typing.List[str] = download_list
        else:
            self.__download_list: typing.List[str] = [
                "https://www.pjf.mg.gov.br/secretarias/sarh/edital/interno/selecao2013/2013/material_de_estudo/matematica/anexos/exercicios.pdf",
                "https://www.c7s.com.br/wp-content/uploads/2019/07/Matem%C3%A1tica-7%C2%B0-ano.pdf",
                "https://colegiosantoantoniorj.com.br/wp-content/uploads/2020/03/Lista-1-de-exerc%C3%ADcios-de-Matem%C3%A1tica-6-ano.pdf",
                "https://projetomedicina.com.br/wp-content/uploads/2016/03/matematica_basica.pdf",
                "http://educacao.varzeadapalma.mg.gov.br/MF%207%C2%BA%20ano%20-%20Matem%C3%A1tica%20ok.pdf",
                "https://icjcoracaodejesus.com.br/uploads/GH16A%20-%20Lista%204%20-%20Divis%C3%A3o.pdf",
                "https://www.colegiogeracao.com.br/wp-content/uploads/2019/02/lista-aula-extra-9-ano.pdf",
                "http://www.escolasapereira.com.br/storage/post_arquivos/634/17307_Mat_1.pdf",
                "https://pirai.rj.gov.br/sme/ensino_fundamental_8_ano/matematica/LISTA%20DE%20EXERC%C3%8DCIOS%20%20-%20%208%C2%BA%20ANO%20%20-%20%20MATEM%C3%81TICA%20%20-%202%C2%AA%20FASE.pdf",
                "https://www.ribeiraocorrente.sp.gov.br/DownloadServlet?id=og1lnn6pwxq6c7d48m4vx6xo9rybjsml"
            ]

        self.__pdfs: str = destination

    def __create_dir_if_not_exist(self) -> None:
        try:
            os.mkdir(f"../{self.__pdfs}")
        except FileNotFoundError:
            ...
        except FileExistsError:
            ...

    async def run(self) -> None:
        """Executa os downloads"""
        self.__create_dir_if_not_exist()
        try:
            async with aiohttp.ClientSession() as session:
                for index, url in enumerate(self.__download_list):
                    cprint(f"[+] Trying download pdf {url}", "yellow", "on_green")
                    async with session.get(url=url, ssl=False) as response:
                        content = await response.read()
                        async with aiofiles.open(f"../{self.__pdfs}/{index}.pdf", "wb") as f:
                            await f.write(content)
                            cprint("[+] PDF saved successfully", "green", "on_yellow")
        except Exception as e:
            cprint(f"[-] ERROR: {e}", "red", "on_black")


if __name__ == '__main__':
    download: Downloader = Downloader()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download.run())
