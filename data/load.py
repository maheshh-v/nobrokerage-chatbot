import pandas as pd
import os

def load_property_data():
    """
    Load and merge all property CSV files
    Returns merged dataframe with all property information
    """
    # Get the directory of this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load CSV files
    project = pd.read_csv(os.path.join(base_dir, "project.csv"))
    address = pd.read_csv(os.path.join(base_dir, "ProjectAddress.csv"))
    config = pd.read_csv(os.path.join(base_dir, "ProjectConfiguration.csv"))
    variant = pd.read_csv(os.path.join(base_dir, "ProjectConfigurationVariant.csv"))
    
    # Merge all dataframes
    df = project.merge(address, left_on="id", right_on="projectId", how="left", suffixes=('', '_addr'))
    df = df.merge(config, left_on="id", right_on="projectId", how="left", suffixes=('', '_config'))
    df = df.merge(variant, left_on="id_config", right_on="configurationId", how="left", suffixes=('', '_variant'))
    
    return df

if __name__ == "__main__":
    # Test data loading
    df = load_property_data()
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nSample data:")
    print(df[['projectName', 'type', 'price', 'status']].head())