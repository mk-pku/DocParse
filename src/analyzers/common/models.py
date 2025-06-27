import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class LayoutBlock:
	box: Tuple[int, int, int, int]
	label: str
	score: float


@dataclass
class LayoutResult:
	original_image: np.ndarray = field(repr=False)
	blocks: List[LayoutBlock] = field(default_factory=list)

	def save_result_image(self, output_path: str, box_width: int = 2, font_size: float = 0.4):
		img = self.original_image.copy()
		font = cv2.FONT_HERSHEY_SIMPLEX
		
		for block in self.blocks:
			x1, y1, x2, y2 = block.box

			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), box_width)
			
			label_text = f"{block.label}: {block.score:.2f}"
			(text_width, text_height), baseline = cv2.getTextSize(label_text, font, font_size, 1)
			
			cv2.rectangle(img, (x1, y1 - text_height - baseline), (x1 + text_width, y1), (0, 255, 0), -1)
			cv2.putText(img, label_text, (x1, y1 - baseline), font, font_size, (0, 0, 0), 1, cv2.LINE_AA)
			
		if img.shape[2] == 3:
			img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

		cv2.imwrite(output_path, img)