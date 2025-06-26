import os
from document_parser import DocumentParser
from paddleocr_parser import PaddleOCRParser


# --- 設定 ---
DATA_DIR = './ocr_data'
IMAGE_NAME = 'sample.png'
# --- 設定ここまで ---

image_full_path = os.path.join(DATA_DIR, IMAGE_NAME)

# --- 使用するパーサーを選択 ---
# ここでインスタンス化するクラスを切り替えるだけで、
# 使用するOCRライブラリを変更できる。
# parser: DocumentParser = TesseractParser() # Tesseractを使う場合
parser: DocumentParser = PaddleOCRParser(use_gpu=False)

# --- 処理の実行 ---
# どの具象クラスでも、同じ'parse'メソッドで呼び出せる
parser.parse(image_full_path)
