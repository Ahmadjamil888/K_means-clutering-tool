# 🤖 AI-Powered K-Means Clustering Tool

A complete Python application for performing K-Means clustering on CSV datasets, available both as a web application and a standalone command-line tool.

## Features

- **Easy CSV Upload**: Upload your dataset through a beautiful web interface or command line
- **Smart Feature Selection**: Automatically detects numeric columns and lets you choose which ones to use
- **Data Standardization**: Uses StandardScaler to normalize your data for optimal clustering
- **Interactive Clustering**: Choose the number of clusters (K) and run K-Means algorithm
- **Visual Results**: Generates scatter plots showing cluster assignments (for 2+ features)
- **Export Results**: Download your clustered dataset with new "Cluster" column
- **Detailed Analysis**: View cluster statistics and data distribution

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Web Application (Recommended)

1. Start the Flask web server:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Follow the step-by-step interface:
   - Upload your CSV file
   - Select numeric columns for clustering
   - Choose number of clusters
   - View results and download clustered dataset

### Command Line Tool

Run the standalone Python script:
```bash
python clustering_tool.py
```

Follow the interactive prompts to:
1. Enter your CSV file path
2. Select features for clustering
3. Choose number of clusters
4. View results and generated files

## How It Works

1. **Data Loading**: Reads your CSV file and displays basic information
2. **Feature Selection**: Shows available numeric columns for clustering
3. **Data Preprocessing**: Handles missing values and standardizes features using StandardScaler
4. **K-Means Clustering**: Applies scikit-learn's K-Means algorithm with your chosen K
5. **Results**: Adds a "Cluster" column to your dataset with cluster assignments
6. **Visualization**: Creates scatter plots using the first two selected features
7. **Export**: Saves results as "clustered_dataset.csv"

## File Structure

```
├── app.py                 # Flask web application
├── clustering_tool.py     # Standalone command-line tool
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
└── README.md             # This file
```

## Example Workflow

1. **Upload Data**: Load a CSV with numeric columns (e.g., customer data, sensor readings)
2. **Select Features**: Choose relevant columns (e.g., age, income, spending_score)
3. **Set Parameters**: Choose number of clusters (e.g., K=3 for customer segments)
4. **Run Clustering**: Algorithm groups similar data points together
5. **Analyze Results**: View cluster distribution and visualization
6. **Export**: Download your data with new cluster labels

## Requirements

- Python 3.7+
- pandas
- scikit-learn
- matplotlib
- flask (for web version)
- numpy

## Error Handling

The tool includes comprehensive error handling for:
- Invalid file paths or formats
- Non-numeric columns
- Missing values (automatically filled with column means)
- Invalid cluster numbers
- File I/O errors

## Tips for Best Results

- Use numeric columns that are meaningful for clustering
- Consider the scale of your features (the tool handles this automatically)
- Start with 2-5 clusters and experiment
- Ensure your dataset has enough rows (at least 10x the number of clusters)
- Remove or handle outliers in your data beforehand if needed

## Output Files

- `clustered_dataset.csv`: Your original data with added "Cluster" column
- `clustering_results.png`: Scatter plot visualization (command-line version)

## License

This project is open source and available under the MIT License.