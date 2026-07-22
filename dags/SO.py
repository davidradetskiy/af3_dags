from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)

default_args = {
    "owner": "dradetsky",
    "depends_on_past": False,
    "retries": 1,
    "email_on_failure": False,
}


spark_pi_manifest = {
    "apiVersion": "sparkoperator.k8s.io/v1beta2",
    "kind": "SparkApplication",
    "metadata": {
        "name": "spark-pi-operator",
    },
    "spec": {
        "type": "Python",
        "pythonVersion": "3",
        "mode": "cluster",
        "image": "radetskiy/spark-app:1.0",
        "imagePullPolicy": "IfNotPresent",
        "mainApplicationFile": "local:///opt/jobs/app.py",
        "sparkVersion": "3.5.0",
        "driver": {
            "cores": 1,
            "memory": "512m",
            "serviceAccount": "spark-operator-sa",
            "labels": {"app": "spark-pi"},
        },
        "executor": {
            "cores": 1,
            "memory": "512m",
            "instances": 1,
            "labels": {"app": "spark-pi"},
        },
        "restartPolicy": {"type": "Never"},
    },
}

with DAG(
    dag_id="spark_kubernetes_operator_simple_test",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["spark", "kubernetes", "operator", "example"],
) as dag:
    start = EmptyOperator(task_id="start")

run_spark_pi = SparkKubernetesOperator(
    task_id="run_spark_pi",
    kubernetes_conn_id="spark_operator_conn",
    namespace="spark-jobs",
    do_xcom_push=False,
    template_spec=spark_pi_manifest,
)

end = EmptyOperator(task_id="end")

start >> run_spark_pi >> end
