import abc
from common.models import LayoutResult


class AbstractLayoutAnalyzer(abc.ABC):
    @abc.abstractmethod
    def analyze(self, image_path: str) -> LayoutResult:
        """
        指定された画像を解析し、統一されたLayoutResult形式で結果を返す。

        Args:
                image_path (str): 解析対象の画像ファイルパス。

        Returns:
                LayoutResult: 解析結果。
        """
        raise NotImplementedError
