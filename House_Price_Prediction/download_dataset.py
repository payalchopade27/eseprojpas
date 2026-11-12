"""
Dataset download script for the Real Estate Valuation dataset.
UCI ML Repository, ID 477.
Run using the project virtual environment.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(project_root, "data", "raw", "real_estate_valuation.csv")

print("=" * 60)
print("Real Estate Valuation Dataset Downloader")
print("UCI ML Repository — Dataset ID 477")
print("=" * 60)

try:
    from ucimlrepo import fetch_ucirepo
    print("\n[1/3] Fetching dataset from UCI ML Repository (ID=477)...")
    real_estate = fetch_ucirepo(id=477)

    X = real_estate.data.features
    y = real_estate.data.targets

    print(f"      Features shape : {X.shape}")
    print(f"      Target shape   : {y.shape}")

    # Combine into a single dataframe
    import pandas as pd
    df = pd.concat([X, y], axis=1)

    # Attempt to retrieve the identifier column if available
    # ucimlrepo sometimes includes IDs in real_estate.data.ids
    try:
        ids = real_estate.data.ids
        if ids is not None and not ids.empty:
            df = pd.concat([ids, df], axis=1)
            print(f"      ID column(s) prepended: {list(ids.columns)}")
    except Exception:
        pass

    print(f"\n[2/3] Combined dataframe shape: {df.shape}")
    print(f"      Columns: {list(df.columns)}")

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"\n[3/3] Dataset saved to: {save_path}")

    # Quick verification
    df_check = pd.read_csv(save_path)
    print(f"\nVerification:")
    print(f"  Rows    : {len(df_check)}")
    print(f"  Columns : {len(df_check.columns)}")
    print(f"  Missing : {df_check.isnull().sum().sum()}")
    print(f"  Duplicates: {df_check.duplicated().sum()}")
    print("\nColumn names and dtypes:")
    print(df_check.dtypes)
    print("\nFirst 3 rows:")
    print(df_check.head(3))
    print("\nDescriptive statistics:")
    print(df_check.describe())

    if len(df_check) == 414:
        print("\n✅ Row count matches expected: 414")
    else:
        print(f"\n⚠️  Row count {len(df_check)} differs from expected 414 — investigate!")

    print("\n✅ Dataset download and verification complete.")

except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("   Make sure ucimlrepo is installed: pip install ucimlrepo")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    sys.exit(1)

