from pathlib import Path
import json


class Config:
    def __init__(self) -> None:
        self._curr_dir = Path(__file__).parent
        
        with open(self._curr_dir / 'config.json', 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def __getitem__(self, key):
        item = self._data[key]
        if key.endswith('_path'):
            item = self._curr_dir / item
        return item