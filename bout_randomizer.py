import numpy as np
import pandas as pd
import os
import fastparquet
from itertools import permutations

from FileCurtain import FileCurtain

'For randomizing sequences to compare transition frequencies. Start/End not to be used.'

class BoutRandomizer():

    def __init__(self, data, vid_limit: int, r_seed: int):
        self.data_fname = data
        self.vid_limit = vid_limit
        self.r_seed = r_seed

        if type(data) == str:
            if self.data_fname.endswith('.parquet'):
                self.data = pd.read_parquet(self.data_fname, engine='fastparquet')
            elif self.data_fname.endswith('.csv'):
                self.data = pd.read_csv(self.data_fname)
        elif type(data) == pd.DataFrame:
            self.data = data

        self.vid_ind = None if self.vid_limit == None else list(range(0, int(self.vid_limit)))
        self.names = np.unique(self.data['Video_name'])

        self.data = self.limit_videos()

    def limit_videos(self):
        
        if self.vid_ind != None and len(self.vid_ind) > 0:
            self.names = self.names[self.vid_ind]
            return self.data[self.data['Video_name'].isin(self.names)]
        else:
            print('Videos are unlimited!')
            return
    
    def randomize(self, groupby: list, state='ordered'):
        """
        Shuffles entire rows within the specified groups.
        All columns (Duration, State, etc.) remain linked to the row.
        """
        rng = np.random.default_rng(seed=self.r_seed)
        shuffled_df = self.data.groupby(groupby, group_keys=False).sample(frac=1, random_state=rng)
        shuffled_df = shuffled_df.reset_index(drop=True)

        return shuffled_df
    
    def export(self, random_data, state_type, save_type = 'parquet'):
        os.makedirs('../library/randomized_data', exist_ok=True)
        state_type = 'ord' if state_type == None else state_type
        data_name = self.data_fname.split('/')[-1].split('.')[0]
        #target_name = target_lib_fname.split('/')[-1].split('.')[0]
        #state_type = 'filt' if self.use_filt_state else 'ord'
        fname = f'lim{self.vid_limit}_{state_type}_@_{data_name}'

        if save_type == 'csv':
            os.makedirs('../library/randomized_data/CSV', exist_ok=True)
            save_path = os.path.join('../library/randomized_data/CSV', 'PERM_' + fname + '.csv')
            random_data.to_csv(save_path, index=False, float_format='%.4f')
        elif save_type == 'parquet':
            os.makedirs('../library/randomized_data/PARQUET', exist_ok=True)    
            save_path = os.path.join('../library/randomized_data/PARQUET', 'PERM_' + fname + '.parquet')
            random_data.to_parquet(save_path, index=False, engine='fastparquet', object_encoding="json")

        return save_path
        

if __name__ == "__main__":
    data_fpath = input("data fpath: ")
    vid_limit = int(input('video limit: '))
    state_type = input('state_type: (ordered/filtered) ')
    r_seed = int(input('random seed: '))
    save_type = input('save_type: (csv/parquet) ')

    groupby = ['Video_name', 'Bout'] #if groupby == None else groupby

    randomizer = BoutRandomizer(data=data_fpath,
                                vid_limit=vid_limit,
                                r_seed=r_seed)
    permuted_data = randomizer.randomize(groupby, state=state_type)
    save_path = randomizer.export(permuted_data, state_type, save_type)

    print(f'Saved data to -> {save_path}')