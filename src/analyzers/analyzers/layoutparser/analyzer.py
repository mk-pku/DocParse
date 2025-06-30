from pathlib import Path
import cv2
from common.base import AbstractLayoutAnalyzer
from common.models import LayoutResult, LayoutBlock
import layoutparser as lp


class LayoutParserAnalyzer(AbstractLayoutAnalyzer):
    def __init__(self, score_thresh: float = 0.8):
        analyzer_dir = Path(__file__).resolve().parent
        config_path = (
            "/app/models/layoutparser/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-config.yml"
        )
        model_path = "/app/models/layoutparser/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-model_final.pth"

        self.model = lp.Detectron2LayoutModel(  # type: ignore
            config_path=config_path,
            model_path=model_path,
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", score_thresh],
        )

    def analyze(self, image_path: str) -> LayoutResult:
        img_bgr = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        result = self.model.detect(img_rgb)

        blocks = []
        for block in result:
            coords = tuple(int(c) for c in block.coordinates)
            if len(coords) != 4:
                raise ValueError(f"Invalid block coordinates: {block.coordinates}")
            blocks.append(LayoutBlock(box=coords, label=block.type, score=block.score))

        return LayoutResult(blocks=blocks, original_image=img_rgb)
