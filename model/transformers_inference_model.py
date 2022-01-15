import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from torch.utils.data import IterableDataset, DataLoader
import os
import json
from typing import Tuple, List, Dict



class TransformersInferenceModel:
    def __init__(self, path: str, max_seq_len: int = 128, device: str = 'cpu', batch_size: int = 1):
        self.model: SentenceTransformer = AutoModel.from_pretrained(path)
        # self.label_map = {i: f'B-{i}' for i in range(self.model.num_labels)}
        self.update_from_model_args(path)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.max_seq_len = max_seq_len
        self.batch_size = batch_size

        if device.startswith('cuda'):
            assert torch.cuda.is_available(), 'torch does not see any cuda'

        self.device = device
        self.model.to(self.device)


    # returns text label
    def predict(self, text: str) -> str:
        pass