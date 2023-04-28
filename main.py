#!bin/bash/env python3
from analyzer import Analyzer


# main.py [-h] -f FILE -a AUTHOR

if __name__ == '__main__':
    a = Analyzer(*Analyzer.get_pdf_path())
    a.start()
