import cv2
from base import AbstractLayoutAnalyzer
from common import LayoutResult, LayoutBlock
from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download

class DocLayoutAnalyzer(AbstractLayoutAnalyzer):
	def __init__(self, conf: float = 0.25):
		ckpt_path = hf_hub_download(
			repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
			filename="doclayout_yolo_docstructbench_imgsz1024.pt"
		)
		self.model = YOLOv10(ckpt_path)
		self.conf = conf
		self.class_names = self.model.model.names

	def analyze(self, image_path: str) -> LayoutResult:
		results = self.model.predict(
			image_path,
			imgsz=1024,
			conf=self.conf,
			device='cpu',
		)

		result = results[0]
		img_bgr = result.orig_img
		img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

		blocks = []
		for box in result.boxes:
			coords = box.xyxy[0].int().tolist()
			blocks.append(
				LayoutBlock(
					box=tuple(coords),
					label=self.class_names[int(box.cls)],
					score=float(box.conf)
				)
			)
		
		return LayoutResult(blocks=blocks, original_image=img_rgb)