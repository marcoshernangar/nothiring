from __future__ import annotations

from kedro.pipeline import Pipeline, node
from nothiring.pipelines.utils.import_drive import descargar_dataset_drive

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=descargar_dataset_drive,
                inputs=dict(
                    output_path="params:drive.output_path",
                    file_id="params:drive.file_id",
                ),
                outputs=None,
                name="descargar_dataset_node",
            )
        ]
    )

