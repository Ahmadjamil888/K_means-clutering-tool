import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variable to store the current dataset
current_dataset = None
original_dataset = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_dataset, original_dataset
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Read the CSV file
        df = pd.read_csv(file)
        current_dataset = df.copy()
        original_dataset = df.copy()
        
        # Get basic info about the dataset
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'head': df.head().to_dict('records'),
            'dtypes': df.dtypes.astype(str).to_dict()
        }
        
        return jsonify({
            'success': True,
            'message': f'Dataset loaded successfully! Shape: {df.shape}',
            'data': info
        })
        
    except Exception as e:
        return jsonify({'error': f'Error loading file: {str(e)}'}), 500

@app.route('/cluster', methods=['POST'])
def perform_clustering():
    global current_dataset
    
    try:
        if current_dataset is None:
            return jsonify({'error': 'No dataset loaded'}), 400
        
        data = request.json
        selected_columns = data.get('columns', [])
        n_clusters = data.get('n_clusters', 3)
        
        if not selected_columns:
            return jsonify({'error': 'Please select at least one column'}), 400
        
        if n_clusters < 2:
            return jsonify({'error': 'Number of clusters must be at least 2'}), 400
        
        # Check if selected columns exist and are numeric
        numeric_columns = []
        for col in selected_columns:
            if col not in current_dataset.columns:
                return jsonify({'error': f'Column "{col}" not found'}), 400
            if not pd.api.types.is_numeric_dtype(current_dataset[col]):
                return jsonify({'error': f'Column "{col}" is not numeric'}), 400
            numeric_columns.append(col)
        
        # Extract features for clustering
        X = current_dataset[numeric_columns].copy()
        
        # Handle missing values
        if X.isnull().any().any():
            X = X.fillna(X.mean())
        
        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to the dataset
        current_dataset['Cluster'] = cluster_labels
        
        # Save the clustered dataset
        output_path = 'clustered_dataset.csv'
        current_dataset.to_csv(output_path, index=False)
        
        # Create visualization if at least 2 features are selected
        plot_data = None
        if len(numeric_columns) >= 2:
            plot_data = create_cluster_plot(X, cluster_labels, numeric_columns[:2])
        
        # Get cluster statistics
        cluster_stats = current_dataset.groupby('Cluster').size().to_dict()
        
        return jsonify({
            'success': True,
            'message': f'Clustering completed! {n_clusters} clusters created.',
            'cluster_stats': cluster_stats,
            'plot': plot_data,
            'clustered_data': current_dataset.head(10).to_dict('records')
        })
        
    except Exception as e:
        return jsonify({'error': f'Error during clustering: {str(e)}'}), 500

def create_cluster_plot(X, cluster_labels, feature_names):
    """Create a scatter plot of the first two features colored by cluster"""
    try:
        plt.figure(figsize=(10, 8))
        
        # Create scatter plot
        unique_clusters = np.unique(cluster_labels)
        colors = plt.cm.Set1(np.linspace(0, 1, len(unique_clusters)))
        
        for i, cluster in enumerate(unique_clusters):
            mask = cluster_labels == cluster
            plt.scatter(X.iloc[mask, 0], X.iloc[mask, 1], 
                       c=[colors[i]], label=f'Cluster {cluster}', alpha=0.7)
        
        plt.xlabel(feature_names[0])
        plt.ylabel(feature_names[1])
        plt.title('K-Means Clustering Results')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plot_data = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return plot_data
        
    except Exception as e:
        print(f"Error creating plot: {e}")
        return None

@app.route('/download')
def download_file():
    try:
        return send_file('clustered_dataset.csv', as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

@app.route('/reset')
def reset_dataset():
    global current_dataset, original_dataset
    if original_dataset is not None:
        current_dataset = original_dataset.copy()
        return jsonify({'success': True, 'message': 'Dataset reset successfully'})
    return jsonify({'error': 'No original dataset to reset to'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)