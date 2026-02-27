"""
Product Clustering ML Pipeline
"""
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator


def load_data(**kwargs):
    """
    Load product data from CSV file
    """
    print("Loading product data...")

    # Load the CSV file
    df = pd.read_csv('/opt/airflow/data/products.csv')

    print(f"Loaded {len(df)} products")
    print(f"Columns: {df.columns.tolist()}")

    # Serialize and return data
    data_serialized = pickle.dumps(df)
    return data_serialized


def data_preprocessing(data, **kwargs):
    """
    Preprocess product data for clustering
    """
    print("Preprocessing data...")

    # Deserialize data
    df = pickle.loads(data)

    # Select features for clustering
    # We'll use: price, rating, and purchase_count
    features = ['price', 'rating', 'purchase_count']
    X = df[features]

    print(f"Selected features: {features}")
    print(f"Data shape: {X.shape}")

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the scaler for later use
    with open('/opt/airflow/working_data/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("Data preprocessing complete!")

    # Return serialized scaled data and original dataframe
    result = {
        'X_scaled': X_scaled,
        'original_df': df
    }

    return pickle.dumps(result)


def build_save_model(data, filename, **kwargs):
    """
    Build K-Means clustering model and find optimal clusters
    """
    print("Building clustering model...")

    # Deserialize data
    result = pickle.loads(data)
    X_scaled = result['X_scaled']

    # Calculate SSE for different numbers of clusters (elbow method)
    sse_values = []
    k_range = range(2, 11)

    print("Finding optimal number of clusters...")
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        sse_values.append(kmeans.inertia_)
        print(f"K={k}, SSE={kmeans.inertia_:.2f}")

    # Find the elbow point
    kl = KneeLocator(
        list(k_range),
        sse_values,
        curve='convex',
        direction='decreasing'
    )

    optimal_k = kl.elbow if kl.elbow else 4
    print(f"\nOptimal number of clusters: {optimal_k}")

    # Train final model with optimal K
    final_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    final_model.fit(X_scaled)

    # Save the model
    model_path = f'/opt/airflow/working_data/{filename}'
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)

    print(f"Model saved to {model_path}")

    return pickle.dumps(sse_values)


def load_model_elbow(filename, sse, **kwargs):
    """
    Load the model and display clustering results
    """
    print("Loading model and generating results...")

    # Deserialize SSE values
    sse_values = pickle.loads(sse)

    # Load the saved model
    model_path = f'/opt/airflow/working_data/{filename}'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    print(f"Model loaded from {model_path}")
    print(f"Number of clusters: {model.n_clusters}")
    print(f"Model inertia: {model.inertia_:.2f}")

    # Load the scaler and original data
    with open('/opt/airflow/working_data/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Load original product data
    df = pd.read_csv('/opt/airflow/data/products.csv')

    # Preprocess and predict clusters
    features = ['price', 'rating', 'purchase_count']
    X = df[features]
    X_scaled = scaler.transform(X)

    # Predict clusters
    df['cluster'] = model.predict(X_scaled)

    # Display cluster statistics
    print("\n=== CLUSTER ANALYSIS ===")
    for cluster_id in range(model.n_clusters):
        cluster_products = df[df['cluster'] == cluster_id]
        print(f"\nCluster {cluster_id}:")
        print(f"  Products: {len(cluster_products)}")
        print(f"  Avg Price: ${cluster_products['price'].mean():.2f}")
        print(f"  Avg Rating: {cluster_products['rating'].mean():.2f}")
        print(f"  Avg Purchases: {cluster_products['purchase_count'].mean():.0f}")
        print(f"  Categories: {cluster_products['category'].unique().tolist()}")

    # Save clustered data
    output_path = '/opt/airflow/working_data/clustered_products.csv'
    df.to_csv(output_path, index=False)
    print(f"\nClustered data saved to {output_path}")

    return f"Clustering complete! Created {model.n_clusters} product clusters."