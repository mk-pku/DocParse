from paddleocr import LayoutDetection
from document_parser import DocumentParser


class PaddleOCRParser(DocumentParser):
	def __init__(self):
		self.model = LayoutDetection()

	def parse(self, image_path: str):
		result = self.model.predict(image_path)
		self._save_results(result)

	def _save_results(self, result):
		for res in result:
			res.save_to_img(save_path="output/sample02.png")
			res.save_to_json(save_path="output/sample02.json")


if __name__ == '__main__':
	parser = PaddleOCRParser()
	parser.parse("input/sample02.png")
