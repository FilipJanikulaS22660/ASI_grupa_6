"""Project pipelines."""
from __future__ import annotations
from typing import Dict
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from pipelines import (
    data_processing as dp,
    data_science as ds,
    model_evaluation as me
)


def register_pipelines() -> Dict[str, Pipeline]:
    """
    Registers the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_processing_pipeline = dp.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    model_evaluation_pipeline = me.create_pipeline()


    return {
        "dp": data_processing_pipeline,
        "ds": data_science_pipeline,
        "me": model_evaluation_pipeline,
        "__default__": data_processing_pipeline + data_science_pipeline + model_evaluation_pipeline
    }