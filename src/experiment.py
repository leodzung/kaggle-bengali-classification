from collections import OrderedDict

from catalyst.dl import ConfigExperiment
from sklearn.model_selection import train_test_split

from src.augmentations import train_aug, valid_aug
from src.dataset import BengaliDataset
import pandas as pd


class Experiment(ConfigExperiment):
    def get_datasets(self, stage: str, **kwargs):
        train_csv_name = kwargs.get('train_csv', None)
        df = pd.read_csv("../input/bengaliai-cv19/" + train_csv_name)
        data_folder = kwargs.get('data_folder', None)
        test_run = kwargs.get('test_run', None)
        image_size = kwargs.get('image_size', None)
        if test_run:
            df = df[:2048]
        #transform = get_transforms(kwargs.get('transform', None))
        datasets = OrderedDict()
        if train_csv_name:
            train_transform = valid_aug(image_size)
            valid_transform = valid_aug(image_size)
            train_df, valid_df = train_test_split(df, test_size=0.2, shuffle=True, random_state=65)
            train_set = BengaliDataset(
                df=train_df,
                transform=valid_transform,
                data_folder=data_folder
            )
            valid_set = BengaliDataset(
                df=valid_df,
                transform=valid_transform,
                data_folder=data_folder
            )
            datasets["train"] = train_set
            datasets["valid"] = valid_set
        return datasets

    @staticmethod
    def get_transforms(stage: str = None, mode: str = None):
        if mode == "train":
            return train_aug
        return valid_aug