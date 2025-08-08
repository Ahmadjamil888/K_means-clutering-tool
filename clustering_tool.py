#!/usr/bin/env python3
"""
AI-Powered K-Means Clustering Tool
A complete Python script for clustering CSV datasets using K-Means algorithm.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
import sys

def load_dataset():
    """Load CSV dataset from user input"""
    while True:
        try:
            file_path = input("\nEnter the path to your CSV file: ").strip()
            
            if not os.path.exists(file_path):
                print("❌ File not found. Please check the path and try again.")
                continue
                
            if not file_path.lower().endswith('.csv'):
                print("❌ Please provide a CSV file.")
                continue
                
            df = pd.read_csv(file_path)
            print(f"✅ Dataset loaded successfully!")
            print(f"📊 Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            return df, file_path
            
        except Exception as e:
            print(f"❌ Error loading file: {str(e)}")
            continue

def display_dataset_info(df):
    """Display basic information about the dataset"""
    print("\n" + "="*60)
    print("📋 DATASET OVERVIEW")
    print("="*60)
    
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nData types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col}: {dtype}")
    
    print(f"\n📊 First 5 rows:")
    print(df.head())
    
    print(f"\n📈 Basic statistics:")
    print(df.describe())

def select_features(df):
    """Allow user to select which columns to use for clustering"""
    print("\n" + "="*60)
    print("🎯 FEATURE SELECTION")
    print("="*60)
    
    # Get numeric columns only
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        print("❌ No numeric columns found in the dataset!")
        return None
    
    print("Available numeric columns:")
    for i, col in enumerate(numeric_columns, 1):
        print(f"  {i}. {col}")
    
    while True:
        try:
            selection = input(f"\nEnter column numbers to use (e.g., 1,2,3) or 'all' for all numeric columns: ").strip()
            
            if selection.lower() == 'all':
                selected_columns = numeric_columns
                break
            
            # Parse user input
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            
            # Validate indices
            if any(i < 0 or i >= len(numeric_columns) for i in indices):
                print("❌ Invalid column number(s). Please try again.")
                continue
            
            selected_columns = [numeric_columns[i] for i in indices]
            break
            
        except ValueError:
            print("❌ Invalid input format. Please enter numbers separated by commas.")
            continue
    
    print(f"✅ Selected columns: {selected_columns}")
    return selected_columns

def get_cluster_count():
    """Get the number of clusters from user"""
    while True:
        try:
            k = int(input("\n🎯 Enter the number of clusters (K): "))
            if k < 2:
                print("❌ Number of clusters must be at least 2.")
                continue
            if k > 20:
                print("⚠️  Large number of clusters. Are you sure? (y/n): ", end="")
                if input().lower() != 'y':
                    continue
            return k
        except ValueError:
            print("❌ Please enter a valid integer.")

def perform_clustering(df, selected_columns, n_clusters):
    """Perform K-Means clustering on selected features"""
    print("\n" + "="*60)
    print("🤖 PERFORMING K-MEANS CLUSTERING")
    print("="*60)
    
    # Extract features
    X = df[selected_columns].copy()
    
    # Handle missing values
    if X.isnull().any().any():
        print("⚠️  Found missing values. Filling with column means...")
        X = X.fillna(X.mean())
    
    print(f"📊 Features shape: {X.shape}")
    print("🔄 Standardizing features...")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"🎯 Running K-Means with {n_clusters} clusters...")
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to original dataset
    df_clustered = df.copy()
    df_clustered['Cluster'] = cluster_labels
    
    print("✅ Clustering completed!")
    
    # Display cluster statistics
    cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()
    print(f"\n📊 Cluster distribution:")
    for cluster, count in cluster_counts.items():
        percentage = (count / len(cluster_labels)) * 100
        print(f"  Cluster {cluster}: {count} points ({percentage:.1f}%)")
    
    return df_clustered, X, cluster_labels, scaler, kmeans

def create_visualization(X, cluster_labels, feature_names, n_clusters):
    """Create scatter plot visualization if 2+ features are selected"""
    if len(feature_names) < 2:
        print("⚠️  Need at least 2 features for visualization.")
        return
    
    print(f"\n📈 Creating visualization using {feature_names[0]} and {feature_names[1]}...")
    
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    unique_clusters = np.unique(cluster_labels)
    colors = plt.cm.Set1(np.linspace(0, 1, len(unique_clusters)))
    
    for i, cluster in enumerate(unique_clusters):
        mask = cluster_labels == cluster
        plt.scatter(X.iloc[mask, 0], X.iloc[mask, 1], 
                   c=[colors[i]], label=f'Cluster {cluster}', 
                   alpha=0.7, s=50)
    
    plt.xlabel(feature_names[0], fontsize=12)
    plt.ylabel(feature_names[1], fontsize=12)
    plt.title(f'K-Means Clustering Results (K={n_clusters})', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plot_filename = 'clustering_results.png'
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    print(f"✅ Plot saved as '{plot_filename}'")
    
    # Show plot
    plt.show()

def save_results(df_clustered, original_filename):
    """Save the clustered dataset"""
    output_filename = 'clustered_dataset.csv'
    df_clustered.to_csv(output_filename, index=False)
    print(f"✅ Clustered dataset saved as '{output_filename}'")
    
    # Display sample of clustered data
    print(f"\n📋 Sample of clustered data:")
    print(df_clustered.head(10))

def analyze_clusters(df_clustered, selected_columns):
    """Provide detailed cluster analysis"""
    print("\n" + "="*60)
    print("📊 CLUSTER ANALYSIS")
    print("="*60)
    
    for cluster in sorted(df_clustered['Cluster'].unique()):
        cluster_data = df_clustered[df_clustered['Cluster'] == cluster]
        print(f"\n🎯 Cluster {cluster} ({len(cluster_data)} points):")
        
        # Show statistics for selected features
        cluster_stats = cluster_data[selected_columns].describe()
        print(cluster_stats.round(3))

def main():
    """Main function to run the clustering tool"""
    print("🤖 AI-Powered K-Means Clustering Tool")
    print("="*60)
    print("Welcome! This tool will help you cluster your CSV data using K-Means algorithm.")
    
    try:
        # Step 1: Load dataset
        df, original_filename = load_dataset()
        
        # Step 2: Display dataset information
        display_dataset_info(df)
        
        # Step 3: Select features
        selected_columns = select_features(df)
        if selected_columns is None:
            print("❌ Cannot proceed without numeric columns.")
            return
        
        # Step 4: Get number of clusters
        n_clusters = get_cluster_count()
        
        # Step 5: Perform clustering
        df_clustered, X, cluster_labels, scaler, kmeans = perform_clustering(
            df, selected_columns, n_clusters
        )
        
        # Step 6: Create visualization
        create_visualization(X, cluster_labels, selected_columns, n_clusters)
        
        # Step 7: Save results
        save_results(df_clustered, original_filename)
        
        # Step 8: Detailed analysis
        analyze_clusters(df_clustered, selected_columns)
        
        print("\n" + "="*60)
        print("🎉 CLUSTERING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("Files created:")
        print("  📄 clustered_dataset.csv - Your data with cluster labels")
        print("  📊 clustering_results.png - Visualization plot")
        
        # Ask if user wants to run again
        while True:
            again = input("\n🔄 Would you like to cluster another dataset? (y/n): ").lower()
            if again in ['y', 'yes']:
                print("\n" + "="*80)
                main()  # Recursive call
                break
            elif again in ['n', 'no']:
                print("👋 Thank you for using the AI-Powered K-Means Clustering Tool!")
                break
            else:
                print("Please enter 'y' or 'n'.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
        print("Please check your data and try again.")

if __name__ == "__main__":
    main()