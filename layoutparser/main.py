import cv2
import layoutparser as lp
import numpy as np


image = cv2.imread("input/sample01.png")
image = image[:, :, ::-1] 

model = lp.Detectron2LayoutModel(
	config_path='models/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-config.yml',
    model_path='models/PubLayNet-mask_rcnn_X_101_32x8d_FPN_3x-model_final.pth',
	label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
	extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8]
)

layout = model.detect(image)

print("Detected Layout Blocks:")
print(layout)

draw_img = lp.draw_box(image, layout, box_width=3, show_element_type=True)
draw_img_np = np.array(draw_img)
output_image = cv2.cvtColor(draw_img_np, cv2.COLOR_RGB2BGR)
cv2.imwrite("output/sample01.png", output_image)

print("\nResult saved to output.jpg")