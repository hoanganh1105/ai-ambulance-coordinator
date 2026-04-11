import numpy as np

class SimpleClassifier:
    """
    Dùng chung interface với một số classifier model thuộc thư viện scikit-learn.
    Hiện thực thuật toán Bernoulli Naive Bayes từ con số 0.
    """
    def __init__(self, alpha=1.0):
        """
        Khởi tạo các tham số cho mô hình.
        :param alpha: Hệ số Laplace smoothing (tránh trường hợp xác suất bằng 0)
        """
        self.alpha = alpha
        self.class_log_prior_ = None
        self.feature_log_prob_ = None
        self.feature_log_prob_neg_ = None
        self.classes_ = None
    
    def fit(self, X, y):
        """
        Train mô hình bằng cách tính toán xác suất tiên nghiệm và xác suất hậu nghiệm.
        """
        # Đảm bảo dữ liệu đầu vào là numpy array để tính toán ma trận
        if hasattr(X, "toarray"):
            X = X.toarray()
        else:
            X = np.array(X)
        y = np.array(y)
        
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]

        class_counts = np.zeros(n_classes)
        feature_counts = np.zeros((n_classes, n_features))

        # Đếm tần suất xuất hiện của bệnh và triệu chứng
        for idx, c in enumerate(self.classes_):
            X_c = X[y == c]
            class_counts[idx] = X_c.shape[0]
            feature_counts[idx, :] = np.sum(X_c, axis=0)

        # Tính Log Prior: log P(C)
        total_samples = X.shape[0]
        self.class_log_prior_ = np.log(class_counts / total_samples)

        # Tính Log Likelihood với Laplace Smoothing: log P(x_i | C)
        smoothed_fc = feature_counts + self.alpha
        smoothed_cc = class_counts[:, np.newaxis] + 2 * self.alpha
        
        prob = smoothed_fc / smoothed_cc
        
        self.feature_log_prob_ = np.log(prob)
        self.feature_log_prob_neg_ = np.log(1 - prob)
        
        # scikit-learn thường return self sau khi fit
        return self
        
    def predict(self, X):
        """
        Dự đoán nhãn (bệnh) dựa trên dữ liệu đầu vào (triệu chứng).
        """
        if hasattr(X, "toarray"):
            X = X.toarray()
        else:
            X = np.array(X)
        # Chuyển thành ma trận 2D nếu input chỉ là 1 array 1D (1 mẫu)
        if X.ndim == 1:
            X = X.reshape(1, -1)
            
        # Áp dụng Định lý Bayes: Cộng dồn Log-likelihood
        term_1 = X @ self.feature_log_prob_.T
        term_2 = (1 - X) @ self.feature_log_prob_neg_.T
        
        log_likelihood = term_1 + term_2 + self.class_log_prior_
        
        # Chọn ra class có xác suất cao nhất
        best_class_indices = np.argmax(log_likelihood, axis=1)
        return self.classes_[best_class_indices]
    
    def score(self, X, y):
        """
        Đánh giá độ chính xác (Accuracy) của mô hình.
        Trả về tỉ lệ dự đoán đúng trên tổng số mẫu.
        """
        y = np.array(y)
        y_pred = self.predict(X)
        
        # Tính accuracy cơ bản giống hàm score() của sklearn
        accuracy = np.mean(y_pred == y)
        return float(accuracy)