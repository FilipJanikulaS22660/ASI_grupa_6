"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_hearth_data

...


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_hearth_data,
                inputs="health",
                outputs="preprocessed_health",
                name="preprocess_health_node",
            ),
        ]
    )
