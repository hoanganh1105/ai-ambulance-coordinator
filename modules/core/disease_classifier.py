import numpy as np

class DiseaseClassifier:
    
    # ---------- Initialization ----------
    def __init__(self, model_name: str = "simpleClassifierModel", trained_model_location: str = None):
        """
        Khởi tạo ML model theo tên
        Có thể định nghĩa thêm attribute tuỳ ý

        :param model_name: Chọn model classifier
        :type model_name: str
        :param trained_model_location: đường dẫn đến file lưu model (nếu chọn trained model)
        :type trained_model_location: str
        """
        self.model = DiseaseClassifier.create_classifier_model(model_name, trained_model_location)

    @classmethod
    def create_classifier_model(cls, name: str, trained_model_location: str = None):
        """
        Chọn ML model theo tên.
        Các ML model này nên có cùng interface một số method cơ bản như fit(), predict()
        """
        if name == "sklearnDecisionTreeClassifier":
            try:
                from sklearn.tree import DecisionTreeClassifier
                return DecisionTreeClassifier(random_state=42)
            except:
                raise ImportError("DiseaseClassifier.create_classifier_model(): Trouble importing sklearn")
        elif name == "trainedModel":
            """Load from .joblib files"""
            # TO DO
            return None
        elif name == "simpleClassifierModel":
            try:
                from models.simple_classifier import SimpleClassifier
                return SimpleClassifier()
            except:
                raise ImportError("DiseaseClassifier.create_classifier_model(): Trouble importing models.simple_classifier")
            return None
        raise ValueError(f"DiseaseClassifier.create_classifier_model(): Unknown model name: {name}")
    
    # ---------- Core methods ----------
    def train(self, dataset_path: str):
        """
        Học từ dataset.
        File này được format như dataset mình đang sử dụng.
        Nếu sử dụng dataset khác thì phải đưa về cùng format trước khi gọi hàm này.
        Encode header row và column => gọi hàm fit() của model.
        
        :param dataset_path: đường dẫn tới file dataset (csv).
        :type dataset_path: str
        """
        # TO DO
    

    def predict(self, X: list[str]) -> str:
        """
        Dự đoán bệnh. Gọi predict() của model
        
        :param X: list triệu chứng (có nằm trong file csv dùng để train)
        :type X: list[str]
        :return: tên bệnh (phải có nằm trong file csv dùng để train)
        :rtype: str
        """
        # TO DO

    # ---------- Evaluation ----------
    """
    Định nghĩa thêm một số metric ở đây. VD: accuracy, precision...
    Nếu gọi trước khi train thì raise error.
    Input: không có
    Output: float
    """