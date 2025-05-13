from pathlib import Path
import shutil

def mover_csv_local(origen: str, destino: str) -> None:
    origen_path = Path(origen)
    destino_path = Path(destino)

    destino_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(origen_path, destino_path)
