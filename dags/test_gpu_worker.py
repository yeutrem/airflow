from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import time

DEFAULT_ARGS = {
    "owner": "lelong1406@gmail.com",
    "depends_on_past": True,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "start_date": datetime(2022, 5, 4, 0, 0, 0),
}

def build_gpu_task(**context):
    import torch
    ###CPU
    start_time = time.time()
    a = torch.ones(4000,4000)
    for _ in range(1000000):
        a += a
    elapsed_time = time.time() - start_time
    print('CPU time = ',elapsed_time)

    ###GPU
    start_time = time.time()
    b = torch.ones(400,400).cuda()
    for _ in range(1000000):
        b += b
    elapsed_time = time.time() - start_time
    print('GPU time = ',elapsed_time)

with DAG(
    'test_gpu_worker',
    default_args=DEFAULT_ARGS,
    catchup=False,
    schedule_interval=None
) as dag:

    flag_success = PythonOperator(
        task_id="gpu_cpu_comparison",
        python_callable=build_gpu_task,
        provide_context=True,
        queue='recsys-gpu-worker',
        execution_timeout=timedelta(seconds=1800)
    )
