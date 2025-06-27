import cv2
from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download

ckpt = hf_hub_download(
	repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
	filename="doclayout_yolo_docstructbench_imgsz1024.pt")

model = YOLOv10(ckpt)
results = model.predict(
	"input/sample01.png",
	imgsz=1024,	# 入力解像度
	conf=0.25,	# 信頼度閾値
	device="cpu",	# GPU / CPU
)
annot = results[0].plot(pil=True, line_width=3, font_size=18)
cv2.imwrite("output/sample01.png", annot)
