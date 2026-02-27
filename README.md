# Product Recommendation Clustering Pipeline - MLOps LAB3

## Project Description
An Apache Airflow-based ML pipeline that clusters products for recommendation systems. The pipeline uses K-Means clustering to group similar products based on price, rating, and purchase count, achieving optimal clustering with the elbow method.

## My Modifications
Instead of the standard K-Means clustering example, I created:
- **Product Recommendation System** using real e-commerce data
- **40 products** across 5 categories (Electronics, Furniture, Appliances, Stationery, Sports)
- **4 optimal product clusters** identified using elbow method
- **Automated Airflow pipeline** with 4 tasks
- **Complete workflow orchestration** with Docker

## Dataset
- **Source**: Custom product dataset
- **Total Products**: 40
- **Categories**: Electronics, Furniture, Appliances, Stationery, Sports
- **Features**: product_id, product_name, category, price, rating, purchase_count

## Technologies Used
- **Apache Airflow**: Workflow orchestration
- **Docker & Docker Compose**: Containerization
- **Scikit-learn**: K-Means clustering
- **Pandas**: Data manipulation
- **Kneed**: Elbow method for optimal K
- **Python**: Core programming language

## Clustering Results

### Model Performance
- **Optimal Clusters**: 4
- **Model Inertia**: 27.29
- **Method**: K-Means with Elbow optimization

### Cluster Analysis

**Cluster 0: Mid-Range Products** (21 products)
- Average Price: $64.13
- Average Rating: 4.27
- Average Purchases: 200
- Categories: All categories mixed

**Cluster 1: Premium Products** (1 product)
- Average Price: $999.99
- Average Rating: 4.50
- Average Purchases: 150
- Categories: High-end Electronics (Laptop)

**Cluster 2: High-Value Products** (8 products)
- Average Price: $201.24
- Average Rating: 4.53
- Average Purchases: 160
- Categories: Electronics, Furniture, Appliances, Sports

**Cluster 3: Budget High-Volume Items** (10 products)
- Average Price: $10.19
- Average Rating: 4.10
- Average Purchases: 401
- Categories: Stationery, cheap Electronics

## Airflow Pipeline

### DAG: product_clustering_pipeline

**Tasks:**
1. **load_product_data** - Loads CSV data
2. **preprocess_data** - Scales features and prepares for clustering
3. **build_clustering_model** - Trains K-Means and finds optimal K
4. **analyze_clusters** - Generates cluster analysis and saves results

**Execution Time**: ~35 seconds

## How to Run

### Prerequisites
- Docker Desktop installed and running
- At least 4GB RAM allocated to Docker

### 1. Clone the repository:
```bash
git clone https://github.com/afrah123456/mlops-airflow-product-clustering.git
cd mlops-airflow-product-clustering
```

### 2. Create .env file:
```bash
echo "AIRFLOW_UID=50000" > .env
```

### 3. Initialize Airflow:
```bash
docker compose up airflow-init
```

Wait for "exited with code 0"

### 4. Start Airflow:
```bash
docker compose up
```

Wait for: `"GET /health HTTP/1.1" 200`

### 5. Access Airflow UI:
Open browser: `http://localhost:8080`
- Username: `admin`
- Password: `admin123`

### 6. Run the Pipeline:
1. Find **product_clustering_pipeline** in DAGs list
2. Toggle it ON (switch on left)
3. Click the DAG name
4. Click Play button → "Trigger DAG"
5. Watch tasks turn green!

### 7. View Results:
- Click on **analyze_clusters** task
- Click **Log** to see cluster analysis
- Check `working_data/clustered_products.csv` for full results

## Airflow DAG Workflow
```
load_product_data 
    ↓
preprocess_data 
    ↓
build_clustering_model 
    ↓
analyze_clusters
```

## Features
 Automated ML pipeline with Airflow  
 Docker containerization for reproducibility  
 K-Means clustering with optimal K detection  
 Real product recommendation use case  
 Complete workflow orchestration  
 Data preprocessing and standardization  
 Model persistence and reusability  
 Comprehensive cluster analysis  

## Stopping Airflow

To stop all containers:
```bash
docker compose down
```

To stop and remove all data:
```bash
docker compose down --volumes --remove-orphans
```

## Screenshots
Screenshots of the running pipeline are available in the `output/` folder:
- DAG execution with all tasks successful
- Cluster analysis results
- DAG graph visualization

## Use Cases
This clustering pipeline can be used for:
- **Product Recommendations**: Recommend similar products within clusters
- **Inventory Management**: Group products by price/popularity tiers
- **Marketing Segmentation**: Target different product clusters differently
- **Pricing Strategy**: Analyze price clusters for competitive pricing

## Author
Afrah Fathima

## Course
MLOps (IE-7374) - LAB3
