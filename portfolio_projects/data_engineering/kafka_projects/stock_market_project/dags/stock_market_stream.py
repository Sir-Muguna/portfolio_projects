from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from datetime import datetime, timedelta
import sys
import os
import logging

# Add the scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../include/scripts"))

# Import Kafka producer and consumer scripts
from kafkaproducer import produce_stock_data
from kafkaconsumer import consume_and_upload_to_s3

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

# SSH connection ID
SSH_CONN_ID = "kafka_ssh_connection"

with DAG(
    dag_id="stock_data_pipeline_with_kafka",
    default_args=default_args,
    description="Automated stock data ingestion with Kafka, S3, and Athena",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Start Zookeeper
    start_zookeeper = SSHOperator(
        task_id="start_zookeeper",
        ssh_conn_id=SSH_CONN_ID,
        command=""" 
        if ! pgrep -x "zookeeper-server-start.sh" > /dev/null
        then
            cd /home/ec2-user/kafka_2.12-3.9.0 &&
            nohup bin/zookeeper-server-start.sh config/zookeeper.properties > /home/ec2-user/kafka_2.12-3.9.0/logs/zookeeper_startup.log 2>&1 & 
        else
            echo "Zookeeper is already running"
        fi
        """,
        conn_timeout=600,
        do_xcom_push=False,
    )

    # Start Kafka Broker
    start_kafka_server = SSHOperator(
        task_id="start_kafka_server",
        ssh_conn_id=SSH_CONN_ID,
        command=""" 
        if ! pgrep -x "kafka-server-start.sh" > /dev/null
        then
            cd /home/ec2-user/kafka_2.12-3.9.0 &&
            export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M" &&
            nohup bin/kafka-server-start.sh config/server.properties > /home/ec2-user/kafka_2.12-3.9.0/logs/server_startup.log 2>&1 & 
        else
            echo "Kafka server is already running"
        fi
        """,
        do_xcom_push=False,
    )

    # Run Kafka Producer
    kafka_producer_task = PythonOperator(
        task_id="run_kafka_producer",
        python_callable=produce_stock_data,
    )

    # Run Kafka Consumer
    kafka_consumer_task = PythonOperator(
        task_id="run_kafka_consumer",
        python_callable=consume_and_upload_to_s3,
    )

    # Run Glue Crawler
    glue_crawler_task = GlueCrawlerOperator(
        task_id="run_glue_crawler",
        config={"Name": "stock-data-crawler"},  # Replace with your Glue Crawler name
        aws_conn_id="aws_default",
    )

    # Query Data with Athena
    athena_query_task = AthenaOperator(
        task_id="query_with_athena",
        query="SELECT * FROM stock_data WHERE volume > 10000;",  # Replace with your query
        database='stock_data_db',
        output_location='s3://stock-market-data-sirm/athena-results/',
        aws_conn_id='aws_default',
    )

    # Stop Kafka Broker
    stop_kafka_server = SSHOperator(
        task_id="stop_kafka_server",
        ssh_conn_id=SSH_CONN_ID,
        command=""" 
        if pgrep -x "kafka-server-start.sh" > /dev/null
        then
            cd /home/ec2-user/kafka_2.12-3.9.0 &&
            bin/kafka-server-stop.sh
        else
            echo "Kafka server is not running"
        fi
        """,
        do_xcom_push=False,
    )

    # Stop Zookeeper
    stop_zookeeper = SSHOperator(
        task_id="stop_zookeeper",
        ssh_conn_id=SSH_CONN_ID,
        command=""" 
        if pgrep -x "zookeeper-server-start.sh" > /dev/null
        then
            cd /home/ec2-user/kafka_2.12-3.9.0 &&
            bin/zookeeper-server-stop.sh
        else
            echo "Zookeeper is not running"
        fi
        """,
        do_xcom_push=False,
    )

    # Define task dependencies
    (
        start_zookeeper >>
        start_kafka_server >>
        kafka_producer_task >>
        kafka_consumer_task >>
        glue_crawler_task >>
        athena_query_task >>
        stop_kafka_server >>
        stop_zookeeper
    )
