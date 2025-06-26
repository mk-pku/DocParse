import abc


class DocumentParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, image_path: str):
        """
        指定された画像ファイルを解析する。

        Args:
            image_path (str): 解析対象の画像ファイルへのパス。
        
        Note:
            この例ではメソッド内でファイル保存まで行いますが、より汎用的な設計として、
            解析結果のデータ構造(例: List[Dict])を返し、
            ファイル保存は呼び出し元で行う方が再利用性は高まります。
        """
        raise NotImplementedError