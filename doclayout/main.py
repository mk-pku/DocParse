
from doclayout_analyzer import DocLayoutAnalyzer


def main():
	INPUT_IMAGE = "input/sample01.png"
	OUTPUT_IMAGE = "output/sample01.png"
	
	analyzer = DocLayoutAnalyzer(conf=0.25)
	# analyzer = LayoutParserAnalyzer(score_thresh=0.8)
	# analyzer = PaddleOCRAnalyzer()
	print(f"Using analyzer: {analyzer.__class__.__name__}")

	try:
		layout_result = analyzer.analyze(INPUT_IMAGE)
		
		print(f"Detected {len(layout_result.blocks)} blocks.")
		for i, block in enumerate(layout_result.blocks):
			print(f"  - Block {i+1}: Label={block.label}, Score={block.score:.2f}, Box={block.box}")
			
		layout_result.save_result_image(OUTPUT_IMAGE)
		print(f"Visualization saved to: {OUTPUT_IMAGE}")

	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == '__main__':
	main()