import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_and_save_features(df: pd.DataFrame, output_dir: str = "features"):
    """
    Separates the pre-encoded binary symptoms and targets, encodes the target diseases, 
    and saves the extracted features as .npy files.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Extract Target (y) and Features (X)
    disease_col = df.columns[0]
    y_raw = df[disease_col].values
    
    # Drop the disease column, the rest are symptoms (already in 0/1 format)
    X_raw = df.drop(columns=[disease_col]).values
    
    # 2. Encode target disease strings into integer labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_raw)
    
    # Ensure X is correctly typed for scikit-learn (int8 to save memory)
    X_encoded = X_raw.astype(np.int8) 
    
    # Get vocabulary of symptoms for later reference
    symptoms_vocab = df.columns[1:].values
    
    # 3. Define file paths
    X_path = os.path.join(output_dir, "X_symptoms.npy")
    y_path = os.path.join(output_dir, "y_diseases.npy")
    symptoms_vocab_path = os.path.join(output_dir, "symptoms_vocab.npy")
    disease_classes_path = os.path.join(output_dir, "disease_classes.npy")
    
    # 4. Export features
    np.save(X_path, X_encoded)
    np.save(y_path, y_encoded)
    np.save(symptoms_vocab_path, symptoms_vocab)
    np.save(disease_classes_path, le.classes_)
    
    return X_encoded, y_encoded, symptoms_vocab, le