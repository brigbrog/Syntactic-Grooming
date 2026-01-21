'''
Brian Brogan
Colby College - The Jackson Laboratory

15 January 2025
Grooming Bout Identifier (Bout string)
------------------------
'''

import numpy as np
import pandas as pd
import os

class BoutStringMachine():

    def __init__(self,
                 data_fname: str,
                 vid_limit: int,
                 use_condensed: bool = True
                 ):
        self.use_condensed = use_condensed
        self.data_fname = data_fname
        self.vid_limit = vid_limit
        self.load_data()
        self.limit_data_by_vid(self.vid_limit)

    def set_data_fname(self, data_str):
        self.data_fname = data_str

    def load_data(self):
        self.data = pd.read_csv(self.data_fname, dtype={
                        "bout": "int",
                        "NetworkFilename": "string",
                        "bout_str": "string",
                        "Strain": "string", 
                        "Sex": "string",
                        "bout_condensed": "string",
                        "prematurely_terminated": "int",
                        "incorrectly_initiated": "int",
                        "skipped": "int",
                        "reversed": "int",
                        "correct": "int",
                        "kaleuff_full": "int",
                        "kumar_full": "int",
                        "kumar_nostop": "int"
                        }
                    )
        
    def limit_data_by_vid(self, vid_limit):
        names = list(self.data['NetworkFilename'].unique())
        names = names[:vid_limit]

        self.data = self.data[self.data['NetworkFilename'].isin(names)]
    
    def get_bout_length_df(self, add_cols):
        add_cols.append('NetworkFilename')
        bout_str_slice = self.data['bout_condensed'] if self.use_condensed else self.data['bout_str']
        bout_lengths = bout_str_slice.apply(lambda x: len(x))
        bout_lengths.name = 'bout_length'

        return pd.concat([self.data[add_cols], bout_str_slice, bout_lengths], axis = 1)
    