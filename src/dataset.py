import cv2
import os
import numpy as np
from torch.utils.data import Dataset

from src.utils import load_image


class BengaliDataset(Dataset):

    def __init__(self, df, data_folder, transform):
        self.image_ids = df['image_id'].values
        self.grapheme_roots = df['grapheme_root'].values
        self.vowel_diacritics = df['vowel_diacritic'].values
        self.consonant_diacritics = df['consonant_diacritic'].values
        self.data_folder = data_folder
        self.transform = transform

    def __len__(self):
        return len(self.image_ids)

    def __getitem__(self, idx):
        image_id = self.image_ids[idx]
        grapheme_root = self.grapheme_roots[idx]
        vowel_diacritic = self.vowel_diacritics[idx]
        consonant_diacritic = self.consonant_diacritics[idx]
        image_path = os.path.join(self.data_folder, image_id + '.png')
        image = cv2.imread(image_path, 0)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        if self.transform:
            image = self.transform(image=image)['image']
        image = np.transpose(image, (2, 0, 1)).astype(np.float32)

        return {
            'image': image,
            'name' : image_id,
            'grapheme_root': grapheme_root,
            'vowel_diacritic': vowel_diacritic,
            'consonant_diacritic': consonant_diacritic
        }