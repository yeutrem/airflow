from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.models import Variable
from typing import Iterable, Sequence, Union, Optional

class DpBigQueryExecuteQueryOperator(BigQueryExecuteQueryOperator):


    def __init__(
        self, 
        sql: Union[str, Iterable[str]],
        destination_dataset_table: Optional[str] = None,
        write_disposition: str = "WRITE_EMPTY",
        allow_large_results: bool = False,
        flatten_results: Optional[bool] = None,
        gcp_conn_id: str = "google_cloud_default",
        udf_config: Optional[list] = None,
        use_legacy_sql: bool = True,
        maximum_billing_tier: Optional[int] = None,
        maximum_bytes_billed: Optional[float] = None,
        create_disposition: str = "CREATE_IF_NEEDED",
        schema_update_options: Optional[Union[list,tuple,set]] = None,
        query_params: Optional[list] = None,
        labels: Optional[dict] = None,
        priority: str = "INTERACTIVE",
        time_partitioning: Optional[dict] = None,
        api_resource_configs: Optional[dict] = None,
        cluster_fields: Optional[list] = None,
        location: Optional[str] = None,
        encryption_configuration: Optional[dict] = None,
        impersonation_chain: Optional[Union[str,Sequence[str]]] = None,
        **kwargs):
        BigQueryExecuteQueryOperator.__init__(
            self,
            sql = sql,
            destination_dataset_table = destination_dataset_table,
            write_disposition = write_disposition,
            allow_large_results = allow_large_results,
            flatten_results = flatten_results,
            gcp_conn_id = gcp_conn_id,
            udf_config = udf_config,
            use_legacy_sql = use_legacy_sql,
            maximum_billing_tier = maximum_billing_tier,
            maximum_bytes_billed = maximum_bytes_billed,
            create_disposition = create_disposition,
            schema_update_options = schema_update_options,
            query_params = query_params,
            labels = labels,
            priority = priority,
            time_partitioning = time_partitioning,
            api_resource_configs = api_resource_configs,
            cluster_fields = cluster_fields,
            location=location,
            encryption_configuration=encryption_configuration,
            impersonation_chain=impersonation_chain,
            **kwargs)
        # each owner can have multiple connection to use.
        # Use airflow variable to store mapping: owner => list_of_connection
        if (self.dag.owner is None) or (self.dag.owner == 'airflow'):
            raise Exception("DAG should be filled out owner info")
        owner_connection_mapping = Variable.get("owner_connection_mapping", {}, deserialize_json=True)
        list_of_connection = owner_connection_mapping.get(self.dag.owner, [self.dag.owner])
        if self.gcp_conn_id not in list_of_connection:
            raise Exception(f"owner {self.dag.owner} can only use {list_of_connection} connections.")
        self.pool = self.dag.owner
