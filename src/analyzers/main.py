from pathlib import Path
# from analyzers.doclayout.analyzer import DocLayoutAnalyzer
# from analyzers.layoutparser.analyzer import LayoutParserAnalyzer
from analyzers.paddleocr.analyzer import PaddleOCRAnalyzer


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"


def main():
    input_image_path = str(INPUT_DIR / "TC23000062_001.png")
    output_image_path = str(OUTPUT_DIR / "TC23000062_001.png")

    # analyzer = DocLayoutAnalyzer(conf=0.25)
    # analyzer = LayoutParserAnalyzer(score_thresh=0.8)
    analyzer = PaddleOCRAnalyzer()
    print(f"Using analyzer: {analyzer.__class__.__name__}")

    analyzer_output_dir = OUTPUT_DIR / analyzer.__class__.__name__
    analyzer_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = analyzer_output_dir / input_file.name

    try:
        layout_result = analyzer.analyze(input_image_path)

        print(f"Detected {len(layout_result.blocks)} blocks.")
        for i, block in enumerate(layout_result.blocks):
            print(
                f"  - Block {i + 1}: Label={block.label}, Score={block.score:.2f}, Box={block.box}"
            )

        layout_result.save_result_image(output_image_path)
        print(f"Visualization saved to: {output_image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
