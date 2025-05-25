from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

AIRFLOW_HOME = '/home/palkinegor/airflow'

with DAG(
    'alignment_analysis',
    start_date=datetime(2025, 1, 1),
    schedule="@once"
) as dag:
    
    align = BashOperator(
        task_id='minimap2_alignment',
        bash_command=f'minimap2 -a {AIRFLOW_HOME}/data/ecoli_ref.fna {AIRFLOW_HOME}/data/SRR33602302.fastq > {AIRFLOW_HOME}/results/aligned.sam'
    )

    flagstat = BashOperator(
        task_id='run_flagstat',
        bash_command=f'samtools flagstat {AIRFLOW_HOME}/results/aligned.sam'
    )

    parse_results = BashOperator(
        task_id='parse_results',
        bash_command=f'{AIRFLOW_HOME}/scripts/parser {AIRFLOW_HOME}/results/aligned.sam'
    )

    align >> flagstat >> parse_results