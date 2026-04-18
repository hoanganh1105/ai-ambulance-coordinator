import os
import pandas as pd
import numpy as np
import joblib
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class DiseaseClassifier:
    
    # ---------- Initialization ----------
    def __init__(self, model_name: str = "simpleClassifierModel", trained_model_location: str = None):
        """
        Khởi tạo ML model theo tên
        """
        self.model_name = model_name
        self.model = DiseaseClassifier.create_classifier_model(model_name, trained_model_location)
        
        # Biến lưu trữ vocab và encoder để dùng cho predict
        self.symptoms_vocab = None
        self.label_encoder = None
        
        # Biến lưu trữ tập Test để dùng cho các hàm Evaluate
        self.X_test_sparse = None
        self.y_test = None
        self.is_trained = (trained_model_location is not None)

    @classmethod
    def create_classifier_model(cls, name: str, trained_model_location: str = None):
        """
        Chọn ML model theo tên.
        """
        if name == "sklearnDecisionTreeClassifier":
            try:
                from sklearn.tree import DecisionTreeClassifier
                return DecisionTreeClassifier(random_state=42)
            except:
                raise ImportError("DiseaseClassifier.create_classifier_model(): Trouble importing sklearn")
                
        elif name == "sklearnNaiveBayes":  # <-- Đã thêm "Gà cưng" Naive Bayes vào đây!
            try:
                from sklearn.naive_bayes import BernoulliNB
                return BernoulliNB()
            except:
                raise ImportError("DiseaseClassifier.create_classifier_model(): Trouble importing sklearn")

        elif name == "trainedModel":
            """Load from .joblib files"""
            if not trained_model_location or not os.path.exists(trained_model_location):
                raise FileNotFoundError(f"Không tìm thấy file model tại: {trained_model_location}")
            return joblib.load(trained_model_location)

        elif name == "simpleClassifierModel":
            try:
                from modules.models.simple_classifier import SimpleClassifier # <--- ĐÃ THÊM modules.
                return SimpleClassifier()
            except:
                raise ImportError("DiseaseClassifier.create_classifier_model(): Trouble importing modules.models.simple_classifier")
        
        raise ValueError(f"DiseaseClassifier.create_classifier_model(): Unknown model name: {name}")
    
    # ---------- Core methods ----------
    def train(self, dataset_path: str):
        """
        Học từ dataset (csv).
        Tiến hành encode, chia tập train/test và ép kiểu sparse matrix để tối ưu bộ nhớ.
        """
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Không tìm thấy file dataset: {dataset_path}")
            
        print(f"Đang tải dữ liệu từ {dataset_path}...")
        df = pd.read_csv(dataset_path)
        
        # 1. Trích xuất X (triệu chứng) và y (bệnh)
        disease_col = df.columns[0]
        y_raw = df[disease_col].values
        X_raw = df.drop(columns=[disease_col]).values
        
        # 2. Lưu vocab và Encode target
        self.symptoms_vocab = df.columns[1:].values
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y_raw)
        X_encoded = X_raw.astype(np.int8)
        
        # 3. Chia tập Train/Test (Lưu Test lại để Evaluate)
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42
        )
        
        # 4. Ép kiểu Sparse Matrix (Tối ưu hóa bộ nhớ và tốc độ)
        print("Đang chuyển đổi sang Sparse Matrix để tăng tốc...")
        X_train_sparse = sp.csr_matrix(X_train)
        self.X_test_sparse = sp.csr_matrix(X_test)
        self.y_test = y_test
        
        # 5. Huấn luyện model
        print(f"Đang huấn luyện mô hình {self.model_name}...")
        self.model.fit(X_train_sparse, y_train)
        self.is_trained = True
        
        print("[HOÀN TẤT] Huấn luyện thành công!")

    def predict(self, X: list[str]) -> str:
        """
        Dự đoán bệnh. Chuyển đổi list các chuỗi triệu chứng thành mảng nhị phân.
        """
        if not self.is_trained or self.symptoms_vocab is None or self.label_encoder is None:
            raise RuntimeError("Mô hình chưa được huấn luyện hoặc chưa load vocabulary. Hãy gọi train() trước.")
            
        # 1. Tạo mảng 0 với độ dài bằng tổng số loại triệu chứng
        input_array = np.zeros(len(self.symptoms_vocab), dtype=np.int8)
        
        # 2. Bật bit 1 cho các triệu chứng có trong list X
        for symptom in X:
            if symptom in self.symptoms_vocab:
                # Tìm vị trí (index) của triệu chứng trong vocab
                idx = np.where(self.symptoms_vocab == symptom)[0][0]
                input_array[idx] = 1
            else:
                print(f"[Cảnh báo] Triệu chứng '{symptom}' không có trong từ điển huấn luyện, sẽ bị bỏ qua.")
                
        # 3. Ép kiểu về ma trận thưa 2 chiều
        input_sparse = sp.csr_matrix(input_array.reshape(1, -1))
        
        # 4. Dự đoán và giải mã label
        pred_idx = self.model.predict(input_sparse)[0]
        predicted_disease = self.label_encoder.inverse_transform([pred_idx])[0]
        
        return predicted_disease

    # ---------- Evaluation ----------
    def evaluate(self) -> dict:
        """
        Trả về Dictionary chứa 4 chỉ số: Accuracy, Precision, Recall, F1-Score
        """
        if not self.is_trained or self.X_test_sparse is None:
            raise RuntimeError("Vui lòng gọi train() trước khi đánh giá mô hình.")
            
        print("Đang đánh giá mô hình trên tập Test...")
        y_pred = self.model.predict(self.X_test_sparse)
        
        acc = accuracy_score(self.y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            self.y_test, y_pred, average='weighted', zero_division=0
        )
        
        return {
            "Accuracy": acc,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1
        }