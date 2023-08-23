from datetime import timedelta, datetime
from airflow.models import DAG
from operators.dp_bigquery_execute_query import DpBigQueryExecuteQueryOperator


DEFAULT_ARGS = {
    "owner": "marketing-team",
    "depends_on_past": True,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2022, 5, 4, 0, 0, 0)
}


with DAG(
        "test_webserver_for_marketing_team",
        schedule_interval=None,
        default_args=DEFAULT_ARGS,
        catchup=False,
        max_active_runs=1,
        max_active_tasks=4,
) as dag:

    DpBigQueryExecuteQueryOperator(
        task_id='task1',
        sql="SELECT 1",
        gcp_conn_id="marketing-team"
    )
