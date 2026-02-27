"""
Airflow DAG for Product Clustering Pipeline
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow')
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow
from airflow import configuration as conf

# Enable pickle support for XCom
conf.set('core', 'enable_xcom_pickling', 'True')

# Define default arguments
default_args = {
    'owner': 'afrah',
    'start_date': datetime(2024, 2, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'product_clustering_pipeline',
    default_args=default_args,
    description='Product Recommendation Clustering Pipeline',
    schedule_interval=None,  # Manual trigger
    catchup=False,
)

# Task 1: Load product data
load_data_task = PythonOperator(
    task_id='load_product_data',
    python_callable=load_data,
    dag=dag,
)

# Task 2: Preprocess data
data_preprocessing_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

# Task 3: Build and save clustering model
build_save_model_task = PythonOperator(
    task_id='build_clustering_model',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, "product_clustering_model.pkl"],
    provide_context=True,
    dag=dag,
)

# Task 4: Load model and analyze clusters
load_model_task = PythonOperator(
    task_id='analyze_clusters',
    python_callable=load_model_elbow,
    op_args=["product_clustering_model.pkl", build_save_model_task.output],
    dag=dag,
)

# Set task dependencies
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task

# Allow command-line interaction
if __name__ == "__main__":
    dag.cli()