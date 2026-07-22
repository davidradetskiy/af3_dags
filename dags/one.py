from pendulum import datetime

from airflow import DAG

from airflow.operators.python import PythonOperator

from airflow.operators.empty import EmptyOperator


default_args = {"owner": "David.Radetsky", "depends_on_past": False, "retries": 2}

MOSCOW_TIMEZONE = "Europe/Moscow"


with DAG(
    dag_id="one_v2",
    default_args=default_args,
    start_date=datetime(day=10, month=1, year=2025, tz=MOSCOW_TIMEZONE),
    schedule=None,
    catchup=True,
) as dag:
    empty_start = EmptyOperator(task_id="start")

    def test():
        print(222222)
        print(222222)
        print(222222)

    one = PythonOperator(
        task_id="one_task",
        python_callable=test,
        dag=dag,
        op_kwargs={},
    )

    two = PythonOperator(
        task_id="one_task",
        python_callable=test,
        dag=dag,
        op_kwargs={},
    )

    empty_start >> one >> two
