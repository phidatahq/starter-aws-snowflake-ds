from pathlib import Path

from airflow.models import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.utils.dates import days_ago

DAG_ID = "notebooks_daily"
EMAILS = ["alerts@datateam.co"]

default_task_args = {
    "owner": "airflow",
    "depends_on_past": True,
    "start_date": days_ago(1),
    "email": EMAILS,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
}

notebooks_daily_dir = Path(__file__).parent
workflows_dir = notebooks_daily_dir.parent
notebooks_dir = workflows_dir.parent.joinpath("notebooks")

with DAG(
    dag_id=DAG_ID,
    description="Run notebooks daily",
    default_args=default_task_args,
    tags=["notebooks"],
    catchup=False,
) as dag:

    test_notebook = PapermillOperator(
        task_id="test_notebook",
        input_nb=str(notebooks_dir.joinpath("examples", "test_nb.ipynb")),
        output_nb="/tmp/test_nb_{{ execution_date }}.ipynb",
        parameters={"msg": "Ran from Airflow at {{ execution_date }}!"},
    )
