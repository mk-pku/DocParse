import argparse
from pathlib import Path

# from analyzers.doclayout.analyzer import DocLayoutAnalyzer
from analyzers.layoutparser.analyzer import LayoutParserAnalyzer
# from analyzers.paddleocr.analyzer import PaddleOCRAnalyzer


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a document image and save the layout visualization."
    )
    parser.add_argument(
        "-i", "--image", type=str, required=True, help="Path to the input image file."
    )
    args = parser.parse_args()

    input_image_path = Path(args.image)
    if not input_image_path.is_file():
        print(f"Error: Input file not found at '{input_image_path}'")
        return

    # analyzer = DocLayoutAnalyzer(conf=0.25)
    analyzer = LayoutParserAnalyzer(score_thresh=0.5)
    # analyzer = PaddleOCRAnalyzer()
    print(f"Using analyzer: {analyzer.__class__.__name__}")

    analyzer_output_dir = OUTPUT_DIR / analyzer.__class__.__name__
    analyzer_output_dir.mkdir(parents=True, exist_ok=True)
    output_file = analyzer_output_dir / input_image_path.name

    try:
        layout_result = analyzer.analyze(str(input_image_path))

        print(f"Detected {len(layout_result.blocks)} blocks.")
        for i, block in enumerate(layout_result.blocks):
            print(
                f"  - Block {i + 1}: Label={block.label}, Score={block.score:.2f}, Box={block.box}"
            )

        layout_result.save_result_image(str(output_file))
        print(f"Visualization saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
