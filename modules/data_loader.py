import os
import pandas as pd

def fetch_and_load_data(dataset_id: str = "dhivyeshrk/diseases-and-symptoms-dataset", data_dir: str = "data") -> pd.DataFrame:
    """
    Downloads the dataset from Kaggle via API and loads it into a Pandas DataFrame.
    Ensures data is downloaded directly to the environment without mounting personal cloud storage.
    
    Args:
        dataset_id (str): The Kaggle dataset identifier.
        data_dir (str): The local directory to store the downloaded data.
        
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"Downloading dataset '{dataset_id}' from Kaggle...")
    # The --unzip flag extracts the files automatically
    exit_code = os.system(f"kaggle datasets download -d {dataset_id} -p {data_dir} --unzip")
    
    if exit_code != 0:
        raise RuntimeError("Failed to download dataset. Please verify your Kaggle API credentials.")

    # Locate the CSV file dynamically in case the filename varies
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the extracted dataset.")
        
    csv_path = os.path.join(data_dir, csv_files[0])
    print(f"Successfully located and loaded data from: {csv_path}")
    
    return pd.read_csv(csv_path)