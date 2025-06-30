import argparse
import importlib
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

ANALYZER_MAP = {
    "doclayout": {
        "module_path": "analyzers.doclayout.analyzer",
        "class_name": "DocLayoutAnalyzer",
        "init_params": {"conf": 0.25},
    },
    "layoutparser": {
        "module_path": "analyzers.layoutparser.analyzer",
        "class_name": "LayoutParserAnalyzer",
        "init_params": {"score_thresh": 0.25},
    },
    "paddleocr": {
        "module_path": "analyzers.paddleocr.analyzer",
        "class_name": "PaddleOCRAnalyzer",
        "init_params": {},
    },
}


def get_analyzer(name: str):
    if name not in ANALYZER_MAP:
        raise ValueError(f"Analyzer '{name}' is not supported.")
    config = ANALYZER_MAP[name]
    try:
        module = importlib.import_module(config["module_path"])
        AnalyzerClass = getattr(module, config["class_name"])
        return AnalyzerClass(**config["init_params"])
    except ImportError as e:
        raise ImportError(f"Failed to import analyzer '{name}': {e}") from e
    except AttributeError as e:
        raise AttributeError(
            f"Analyzer class '{config['class_name']}' not found in module '{config['module_path']}': {e}"
        ) from e


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a document image and save the layout visualization."
    )
    parser.add_argument(
        "-i", "--image", type=str, required=True, help="Path to the input image file."
    )
    parser.add_argument(
        "-a",
        "--analyzer",
        type=str,
        required=True,
        choices=list(ANALYZER_MAP.keys()),
        help="The analyzer to use for processing.",
    )
    args = parser.parse_args()

    input_image_path = Path(args.image)
    if not input_image_path.is_file():
        print(f"Error: Input file not found at '{input_image_path}'")
        return

    analyzer = get_analyzer(args.analyzer)
    if not analyzer:
        sys.exit(1)
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
