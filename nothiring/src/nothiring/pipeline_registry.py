from __future__ import annotations
from kedro.pipeline import Pipeline
from nothiring.pipelines.import_data import pipeline as import_data_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "import_data": import_data_pipeline.create_pipeline(),
        "__default__": import_data_pipeline.create_pipeline(),
    }
