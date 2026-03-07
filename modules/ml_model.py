import os
import numpy as np
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class DiseaseClassifier:
    """
    A machine learning pipeline for classifying diseases based on binary symptom arrays.
    Utilizes a Decision Tree Classifier to provide highly interpretable predictions.
    """
    
    def __init__(self, model_dir: str = "features"):
        """
        Initializes the classifier and defines paths for saving/loading the model.
        
        Args:
            model_dir (str): The directory where the trained model and classes are stored.
        """
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, "decision_tree_model.joblib")
        self.classes_path = os.path.join(model_dir, "disease_classes.npy")
        self.model = None
        self.disease_classes = None
        
        os.makedirs(self.model_dir, exist_ok=True)

    def train(self, X_path: str = "features/X_symptoms.npy", y_path: str = "features/y_diseases.npy"):
        """
        Loads extracted features, trains the Decision Tree model, evaluates its performance,
        and saves the trained model to the local directory.
        """
        print("Loading feature matrices for training...")
        if not os.path.exists(X_path) or not os.path.exists(y_path):
            raise FileNotFoundError("Feature files not found. Please run the preprocessor module first.")

        # Load features and target labels
        X = np.load(X_path)
        y = np.load(y_path)
        
        if not os.path.exists(self.classes_path):
            raise FileNotFoundError("Disease classes mapping not found.")
        self.disease_classes = np.load(self.classes_path, allow_pickle=True)

        print(f"Data successfully loaded. X shape: {X.shape}, y shape: {y.shape}")
        
        # Split data into training (80%) and testing (20%) sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize and train the Decision Tree Classifier (Removed max_depth to allow full learning)
        print("Training Decision Tree Classifier... (This might take a minute without depth limits)")
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model performance on the test set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n[TRAINING COMPLETE] Model Accuracy on test set: {accuracy * 100:.2f}%")
        
        # Note: classification_report is removed to prevent console spam and class mismatch errors 
        # caused by rare diseases missing from the 20% test split.
        
        # Save the trained model to disk
        joblib.dump(self.model, self.model_path)
        print(f"Model successfully saved to {self.model_path}")

    def load_trained_model(self):
        """
        Loads the pre-trained model and the disease classes mapping from disk.
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file {self.model_path} not found. Please run train() first.")
        
        self.model = joblib.load(self.model_path)
        self.disease_classes = np.load(self.classes_path, allow_pickle=True)

    def predict_disease(self, symptom_array: np.ndarray) -> str:
        """
        Predicts the most likely disease given a binary array of symptoms.
        
        Args:
            symptom_array (np.ndarray): A 1D or 2D binary array representing presence (1) or absence (0) of symptoms.
            
        Returns:
            str: The name of the predicted disease with the highest probability.
        """
        # Automatically load the model if it hasn't been loaded in this session
        if self.model is None or self.disease_classes is None:
            self.load_trained_model()
            
        # Ensure the input is a 2D array (required by scikit-learn for prediction)
        if symptom_array.ndim == 1:
            symptom_array = symptom_array.reshape(1, -1)
            
        # Perform prediction
        prediction_idx = self.model.predict(symptom_array)[0]
        predicted_disease = self.disease_classes[prediction_idx]
        
        return predicted_disease