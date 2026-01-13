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

class BoutMachine():

    def __init__(self,
                 target_chain: str,
                 use_filt_state: bool = True,
                 use_bout_assignment: bool = False
                 ):
        
        # set controls
        self.phase = 0
        self.chain_acc = 0
        self.target_chain = target_chain
        self.use_filt_state = use_filt_state
        self.use_bout_assignment = use_bout_assignment


    def set_target_chain(self, target_chain: str):
        self.target_chain = target_chain


    def read_state(self, reference):

        # NEED FILTERED STATE SUPPORT

        if self.use_filt_state:
            state_read = int(reference['Filtered_State'])
        else:
            state_read = int(reference['Ordered_State'])

        return state_read
    
    
    def read_bout(self, reference):

        bout = int(reference['Bout'])
        if bout != 0:
            return bout
        
        return None
    

    def verify_state(self, state_read, target_chain, index):

        if int(state_read) == int(target_chain[index]):
            return True
        
        return False
    
    
    def verify_bout(self, previous, current):
        if previous is None or current is None:
            return False

        prev, curr = int(previous), int(current)
        return prev == curr and curr != 0

    
    def single_vid_matchlog(self,
                            video: pd.DataFrame,
                            verbose: bool = False,
                            ):

        identified = 0
        interval_log = {}
        bout_log = {}
        bout_start = 0

        for ref in video.iterrows():
            
            # read the current state in the video
            state_read = self.read_state(ref[1])

            # read the current bout in the video 
            bout_read = self.read_bout(ref[1])

            if verbose:
                print(f'state read: {state_read} chain acc: {self.chain_acc} target val: {self.target_chain[self.chain_acc]} s_verify: {self.verify_state(state_read, self.target_chain, self.chain_acc)}')

            # verify if the read state agrees with current index of target chain
            if self.verify_state(state_read, self.target_chain, self.chain_acc):
                if self.chain_acc == 0: 
                    cur_start = ref[1]['Start']
                    bout_start = ref[1]['Bout'] 

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
                cur_end = ref[1]['End']
                bout_end = ref[1]['Bout']

                if verbose:
                    print(f'MATCH: {(cur_start, cur_end)}')

                interval_log[f'match_{identified}'] = (cur_start, cur_end)
                bout_log[f'match_{identified}'] = (bout_start, bout_end)

                # reset chain accumulator
                self.chain_acc = 0

        return interval_log, bout_log
    
    def pull_match_data(self, data: pd.DataFrame, video: str, match_log: dict, target: str, vid_sidx: int = None):
        '''
        Docstring for pull_match_data
        returns formatted dictionary for multi video searching
        columns: match #, target, interval, bout #, sex, strain, duration
        '''

        toReturn = []
        slice = data[data['Video_name']==video]

        for i, key in enumerate(match_log.keys()):

            interval = match_log[key]

            pull = {
                'target' : target,
                'match_num' : i+1,
                'interval' : interval,
                'bout_num' : slice[slice['Start'] == interval[0]]['Bout'].iloc[0],
                'sex' : slice[slice['Start'] == interval[0]]['Sex'].iloc[0],
                'strain' : slice[slice['Start'] == interval[0]]['Strain'].iloc[0],
                'duration' : slice.loc[(slice['Start'] >= interval[0]) & (slice['End'] <= interval[1]), 'Duration'].to_numpy(),
                'video_search_index' : vid_sidx,
                'video_name' : video
            }

            toReturn.append(pull)

        return pd.DataFrame(toReturn)
        


    def multi_vid_matchlog(self, data: pd.DataFrame, vid_ind: list = None, verbose: bool = False):
        
        mv_match_log = None
        
        names = np.unique(data['Video_name'])
        if vid_ind != None and len(vid_ind) > 0:
            names = names[vid_ind]

        for idx, name in enumerate(names):
            #print(f'searching video {idx}')
            data_slice = data[data['Video_name'] == name]
            match_log = self.single_vid_matchlog(data_slice)

            if verbose:
                print(f'Video # : {idx}')
                print(f'Matches found: {len(match_log[0])}: {match_log[0]}')
                
            toAdd = self.pull_match_data(data_slice, name, match_log[0], self.target_chain, idx)

            if idx == 0:
                mv_match_log = toAdd
            else:
                mv_match_log = pd.concat([mv_match_log, toAdd], ignore_index=True)

        
        return mv_match_log
    
    def get_save_path(self, data_fname, target_lib_fname, vid_limit):
        data_name = data_fname.split('/')[-1].split('.')[0]
        target_name = target_lib_fname.split('/')[-1].split('.')[0]
        filename = f'lim{vid_limit}_{target_name}_@_{data_name}'

        os.makedirs('../library/search_logs', exist_ok=True)
        save_path = os.path.join('../library/search_logs', filename + '.csv')

        return save_path
                

if __name__ == "__main__":
    data_fname = input("data fname: ")
    target_lib_fname = input("target chain library fname: ")
    save_run = input("save run? (y/n): ")
    vid_limit = input("video limit (int or 'all'): ")
    verbose = input('verbose? (y/n): ')
    

    data = pd.read_csv(data_fname)
    toReturn = None

    vid_ind = None if vid_limit.lower() == 'all' else list(range(0, int(vid_limit)))
    
    #print(f'searching {data.shape[0]} states...')
    
    with open(target_lib_fname, 'r') as library:
        lines = (line.strip() for line in library)

        for idx, target in enumerate(lines):
            
            boutMachine = BoutMachine(target, False)
            match_log = boutMachine.multi_vid_matchlog(data, vid_ind=vid_ind)
            if verbose.lower() == 'y': 
                print(f'target {idx+1}: {target} -> {match_log.shape[0]} matches found')
            if idx == 0:
                toReturn = match_log
            else:
                toReturn = pd.concat([toReturn, match_log], ignore_index=True)

    if save_run.lower() == 'y':
        toReturn.to_csv(boutMachine.get_save_path(data_fname, target_lib_fname, vid_limit), index=False)