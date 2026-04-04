from sklearn.tree import DecisionTreeClassifier
import numpy as np
from models.simple_classifier import SimpleClassifierModel

class DiseaseClassifier:
    
    # ---------- Initialization ----------
    def __init__(self, model_name: str = "simpleClassifierModel", trained_model_location: str = None):
        """
        Khởi tạo ML model theo tên
        Có thể định nghĩa thêm attribute tuỳ ý
        """
        # TO DO
        self.model = None

    @classmethod
    def create_classifier_model(cls, name: str, trained_model_location: str = None):
        """
        Trả về ML model theo tên
        """
        if name == "sklearnDecisionTreeClassifier":
            return DecisionTreeClassifier(random_state=42)
        elif name == "trainedModel":
            """Load from .joblib files"""
            # TO DO
            return None
        elif name == "simpleClassifierModel":
            # TO DO
            return None
        raise ValueError(f"DiseaseClassifier.create_classifier_model(): Unknown model name: {name}")
    
    # ---------- Core methods ----------
    def train(self, dataset_path: str):
        """
        Train model.
        Input: đường dẫn tới file dataset (csv)
        Có thể cố định format file input theo một chuẩn nào đó, huyến khích human-readable (header row và column chưa mã hoá thành số)
        """
        # TO DO
    

    def predict(self, X: list[str]) -> str:
        """
        Dự đoán bệnh.
        Input: list[str] -> list triệu chứng (phải có nằm trong file csv dùng để train)
        Output: str -> tên bệnh (phải có nằm trong file csv dùng để train)
        """
        # TO DO

    # ---------- Evaluation ----------
    """
    Định nghĩa thêm một số metric ở đây. VD: accuracy, precision...
    Nếu gọi trước khi train thì raise error.
    Input: không có
    Output: float
    """