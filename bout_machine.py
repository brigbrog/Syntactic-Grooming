'''
Brian Brogan
Colby College - The Jackson Laboratory

3 December 2025
Grooming Bout Identifier
------------------------
'''

import numpy as np
import pandas as pd
import os
import fastparquet

class BoutMachine():

    def __init__(self,
                 target_chain: str,
                 use_filt_state: bool = True,
                 #use_bout_assignment: bool = False
                 ):
        
        #self.phase = 0
        self.chain_acc = 0
        self.target_chain = target_chain
        self.use_filt_state = use_filt_state
        #self.use_bout_assignment = use_bout_assignment


    def set_target_chain(self, target_chain: str):
        '''
        Sets the target chain instance variable
        '''
        self.target_chain = target_chain


    def read_state(self, reference):
        '''
        Reads the state from reference sample using use_filt_state instance variable (bool.
        Returns none if self.use_filt_state & state read is 'X', otherwise int casted state.
        '''
        if self.use_filt_state:
            state_read = reference['Filtered_State']
            if state_read == 'X':
                return None
            else:
                state_read = int(state_read)
        else:
            state_read = int(reference['Ordered_State'])

        return state_read
    
    
    def read_bout(self, reference):
        '''
        Reads the bout from reference sample.
        Returns bout if bout read is nonzero, otherwise None.
        '''
        bout = int(reference['Bout'])
        if bout != 0:
            return bout
        
        return None
    

    def verify_state(self, state_read, target_chain, index):
        '''
        Verifies if the current state read equals the current index of the target chain.
        Returns true if equal, otherwise False.
        '''
        if int(state_read) == int(target_chain[index]):
            return True
        
        return False
    
    
    def verify_bout(self, previous, current):
        '''
        Verifies if the current bout read equals the previous bout read. 
        Returns True if bout reads are nonzero and equal, otherwise False.
        '''
        # revisit for bout start or end check?
        if previous is None or current is None:
            return False

        prev, curr = int(previous), int(current)
        return prev == curr and curr != 0

    
    def single_vid_matchlog(self,
                            video: pd.DataFrame,
                            verbose: bool = False,
                            ):
        '''
        Bout search algorithm for single video analysis.
        
        :param self: Description
        :param video: Data slice for single video
        :param verbose: Bool for process updates
        '''
        identified = 0
        interval_log = {}
        bout_start = 0
        last_state = None

        for idx, ref in video.iterrows():
            
            # read the current state in the video
            state_read = self.read_state(ref)
            if self.use_filt_state and (state_read == None or state_read == last_state):
                continue

            # read the current bout in the video 
            bout_read = self.read_bout(ref)

            if verbose:
                print(f'state read: {state_read} chain acc: {self.chain_acc} target val: {self.target_chain[self.chain_acc]} s_verify: {self.verify_state(state_read, self.target_chain, self.chain_acc)}')

            # verify if the read state agrees with current index of target chain
            if self.verify_state(state_read, self.target_chain, self.chain_acc):
                if self.chain_acc == 0: 
                    cur_start = ref['Start']
                    bout_start = ref['Bout']

                self.chain_acc += 1
                
                if verbose:
                    print(f'bout read: {bout_read}, target val: {bout_start}, b_verify: {self.verify_bout(bout_start, bout_read)}')

                # if the bout is different, the match has failed. Break the chain
                if not self.verify_bout(bout_start, bout_read):
                    if verbose and self.chain_acc > 0:
                        print(f'MATCH FAILED (BOUT): {cur_start}')
                    self.chain_acc = 0
                
            # otherwise reset chain accumulator and start counter    
            else:
                if verbose and self.chain_acc > 0:
                    print(f'MATCH FAILED (STATE): {cur_start}')
                self.chain_acc = 0
                cur_start = np.nan
                bout_start = 0

            # add bout to return field if chain accumulator reaches max
            if self.chain_acc == len(self.target_chain):
                identified += 1
                cur_end = ref['End']

                if verbose:
                    print(f'MATCH: {(cur_start, cur_end)}')

                interval_log[f'match_{identified}'] = (cur_start, cur_end)

                # reset chain accumulator
                self.chain_acc = 0
            
            last_state = state_read

        return interval_log
    
    
    def pull_match_data(self, data: pd.DataFrame, video: str, match_log: dict, target: str, vid_sidx: int = None):
        '''
        returns formatted dataframe for multi video searching
        columns: target, match number, match interval, bout number, bout interval, match position, bout position, duration, sex, strain, video search index, video name
        '''

        toReturn = []
        slice = data[data['Video_name']==video]

        for i, key in enumerate(match_log.keys()):

            match_interval = np.array(match_log[key], dtype=np.int64)
            bout_interval = np.array([slice.loc[slice['Bout'] == slice.loc[slice['Start'] == match_interval[0], 'Bout'].iloc[0], 'Start'].iloc[0],
                                      slice.loc[slice['Bout'] == slice.loc[slice['Start'] == match_interval[0], 'Bout'].iloc[0], 'End'].iloc[-1]], dtype=np.int64)

            pull = {
                'target' : target,
                'match_num' : i+1,
                'match_interval' : match_interval,
                'bout_num' : slice[slice['Start'] == match_interval[0]]['Bout'].iloc[0],
                'bout_interval' : bout_interval,
                'match_pos' : match_interval[0] / slice['End'].iloc[-1], # match start position in video as a percentage of total video length
                'bout_pos' : bout_interval[0] / slice['End'].iloc[-1], # bout start position in video as a percentage of total video length
                'duration' : slice.loc[(slice['Start'] >= match_interval[0]) & (slice['End'] <= match_interval[1]), 'Duration'].to_numpy(),
                'sex' : slice[slice['Start'] == match_interval[0]]['Sex'].iloc[0],
                'strain' : slice[slice['Start'] == match_interval[0]]['Strain'].iloc[0],
                'video_search_index' : vid_sidx,
                'video_name' : video
            }

            toReturn.append(pull)

        return pd.DataFrame(toReturn)
        

    def multi_vid_matchlog(self, data: pd.DataFrame, vid_ind: list = None, verbose: bool = False):
        '''
        Runs bout search algorithm for all specified videos.
        If video indices are None, all videos in dataframe are searched.
        '''
        
        mv_match_log = None
        
        names = np.unique(data['Video_name'])
        if vid_ind != None and len(vid_ind) > 0:
            names = names[vid_ind]

        for idx, name in enumerate(names):
            data_slice = data[data['Video_name'] == name]
            match_log = self.single_vid_matchlog(data_slice)

            if verbose:
                print(f'Video # : {idx}')
                print(f'Matches found: {len(match_log)}: {match_log}')
                
            toAdd = self.pull_match_data(data_slice, name, match_log, self.target_chain, idx)

            mv_match_log = toAdd if idx == 0 else pd.concat([mv_match_log, toAdd], ignore_index=True)
        
        return mv_match_log
    

    def get_save_path(self, data_fname, target_lib_fname, vid_limit, save_type):
        '''
        Generates save name for output data.
        '''
        data_name = data_fname.split('/')[-1].split('.')[0]
        target_name = target_lib_fname.split('/')[-1].split('.')[0]
        state_type = 'filt' if self.use_filt_state else 'ord'
        filename = f'lim{vid_limit}_{target_name}_{state_type}_@_{data_name}'

        os.makedirs('../library/search_logs', exist_ok=True)
    
        if save_type == 'csv':
            os.makedirs('../library/search_logs/CSV', exist_ok=True)
            save_path = os.path.join('../library/search_logs/CSV', filename)
        elif save_type == 'parquet':
            os.makedirs('../library/search_logs/PARQUET', exist_ok=True)    
            save_path = os.path.join('../library/search_logs/PARQUET', filename)
        
        return save_path
                

if __name__ == "__main__":
    data_fname = input("data fname: ")
    target_lib_fname = input("target chain library fname: ")
    save_run = input("save run? (y/n): ")
    save_type = None if save_run.lower() == 'n' else input('save type? (csv/parquet): ').lower()
    vid_limit = input("video limit (int or 'all'): ")
    use_filt_state = input("use filtered states? (y/n): ")
    verbose = input('verbose? (y/n): ')
    
    data = pd.read_csv(data_fname)
    toReturn = None

    vid_ind = None if vid_limit.lower() == 'all' else list(range(0, int(vid_limit)))
    state_type = True if use_filt_state.lower() == 'y' else False
    
    with open(target_lib_fname, 'r') as library:
        lines = (line.strip() for line in library)

        for idx, target in enumerate(lines):
            
            boutMachine = BoutMachine(target, use_filt_state=state_type)
            match_log = boutMachine.multi_vid_matchlog(data, vid_ind=vid_ind)
            if verbose.lower() == 'y': 
                print(f'target {idx+1}: {target} -> {match_log.shape[0]} matches found')

            toReturn = match_log if idx == 0 else pd.concat([toReturn, match_log], ignore_index=True)

    if save_run.lower() == 'y':
        if save_type == 'csv':
            save_path = boutMachine.get_save_path(data_fname, target_lib_fname, vid_limit, save_type) + '.csv'
            toReturn.to_csv(save_path, index=False, float_format='%.4f')
        elif save_type == 'parquet':
            save_path = boutMachine.get_save_path(data_fname, target_lib_fname, vid_limit, save_type) + '.parquet'
            toReturn = toReturn.map(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
            toReturn.to_parquet(save_path, index=False, engine='fastparquet', object_encoding="json")
        else:
            raise ValueError(f'invalid file type for saving: {save_type}')