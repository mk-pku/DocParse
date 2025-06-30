import cv2
from common.base import AbstractLayoutAnalyzer
from common.models import LayoutResult, LayoutBlock
from paddleocr import LayoutDetection  # type: ignore


class PaddleOCRAnalyzer(AbstractLayoutAnalyzer):
    def __init__(self):
        self.model = LayoutDetection()

    def analyze(self, image_path: str) -> LayoutResult:
        img_bgr = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        result = self.model.predict(image_path)

        blocks = []
        detected_boxes = result[0].get("boxes", [])
        for box in detected_boxes:
            coords = tuple(int(c) for c in box["coordinate"])
            if len(coords) != 4:
                raise ValueError(f"Invalid box coordinates: {box['coordinate']}")
            blocks.append(
                LayoutBlock(box=coords, label=box["label"], score=box["score"])
            )

        return LayoutResult(blocks=blocks, original_image=img_rgb)
