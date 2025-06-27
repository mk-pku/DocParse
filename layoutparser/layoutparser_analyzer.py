import cv2
from base import AbstractLayoutAnalyzer
from common import LayoutResult, LayoutBlock
import layoutparser as lp


class LayoutParserAnalyzer(AbstractLayoutAnalyzer):
	def __init__(self, score_thresh: float = 0.8):
		self.model = lp.Detectron2LayoutModel(
			config_path='models/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-config.yml',
			model_path='models/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-model_final.pth',
			label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
			extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", score_thresh]
		)

	def analyze(self, image_path: str) -> LayoutResult:
		img_bgr = cv2.imread(image_path)
		img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
		result = self.model.detect(img_rgb)

		blocks = []
		for block in result:
			coords = [int(c) for c in block.coordinates]
			blocks.append(
				LayoutBlock(
					box=tuple(coords),
					label=block.type,
					score=block.score
				)
			)
		
		return LayoutResult(blocks=blocks, original_image=img_rgb)