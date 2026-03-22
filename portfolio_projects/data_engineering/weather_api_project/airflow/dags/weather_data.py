import sys
from airflow import DAG  # type: ignore
from airflow.operators.python import PythonOperator  # type: ignore
from airflow.providers.docker.operators.docker import DockerOperator  # type: ignore
from datetime import datetime, timedelta
from docker.types import Mount  # type: ignore

# Add path for ingestion script
sys.path.append('/opt/airflow/api-request')
from insert_records import main  # type: ignore

default_args = {
    'description': 'A DAG to orchestrate weather API ingestion and dbt transformation',
    'start_date': datetime(2025, 8, 21),
    'catchup': False,
}

dag = DAG(
    dag_id='Weather-data-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5),
)

with dag:
    # Task 1: Ingest data from API
    ingest_task = PythonOperator(
        task_id='ingest_data',
        python_callable=main,
    )

    # Task 2: Run dbt transformations in Docker
    transform_task = DockerOperator(
        task_id='transform_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(
                source='/root/projects/portfolio_projects/data_engineering/weather_api_project/dbt/my_project',
                target='/usr/app',
                type='bind',
            ),
            Mount(
                source='/root/projects/portfolio_projects/data_engineering/weather_api_project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind',
            ),
        ],
        network_mode='weather_api_project_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success',
    )

    # Set dependencies
    ingest_task >> transform_task # type: ignore
