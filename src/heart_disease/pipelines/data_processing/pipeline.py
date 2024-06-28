"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_hearth_data, download_data

...


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=download_data,
                inputs={
                    "output_filepath": "params:output_filepath",
                    "db_uri": "params:db_uri",
                    "table_name": "params:table_name"
                },
                outputs="raw_data",
                name="download_data",
            ),
            node(
                func=preprocess_hearth_data,
                inputs="raw_data",
                outputs="preprocessed_health",
                name="preprocess_health_node",
            ),
        ]
    )
