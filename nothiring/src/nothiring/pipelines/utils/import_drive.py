import gdown
from pathlib import Path

def descargar_dataset_drive(output_path: str, file_id: str) -> None:
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gdown.download(url, str(output_path), quiet=False)