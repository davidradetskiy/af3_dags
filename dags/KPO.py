from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

default_args = {
    "owner": "dradetsky",
    "depends_on_past": False,
    "retries": 1,
    "email_on_failure": False,
}


with DAG(
    dag_id="kubernetes_operator_simple_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
) as dag:
    start = EmptyOperator(task_id="start")

    kpo = KubernetesPodOperator(
        task_id="populate_target_table",
        in_cluster=True,
        image="radetskiy/kube-app:1.0",
        image_pull_policy="Always",
        name="weather-forecast-hourly",
        cmds=["python", "app.py"],
        get_logs=True,
        container_logs=True,
        log_events_on_failure=True,
    )


end = EmptyOperator(task_id="end")

start >> kpo >> end
