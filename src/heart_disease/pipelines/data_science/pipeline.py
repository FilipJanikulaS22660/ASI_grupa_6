"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, pipeline, node

from .nodes import split_data, train_model, evaluate_model, autoML

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["preprocessed_health"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="random_forest_classifier",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["random_forest_classifier", "X_test", "y_test", "X_train", "y_train"],
                outputs=None,
                name="evaluate_model_node",
            ),
            node(
                func=autoML,
                inputs=["preprocessed_health"],
                outputs="autoML_model",
                name="autoML"
            )
        ]
    )
