'''
Brian Brogan
Colby College - The Jackson Laboratory

3 December 2025
Grooming Bout Identifier
------------------------
'''

import numpy as np
import pandas as pd

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
                            verbose: bool = True,
                            ):

        identified = 0
        interval_log = {}
        bout_log = {}

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
    
    def pull_match_data(self, data: pd.DataFrame, video: str, match_log: dict, target: str):
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
                'target':target,
                'match_num':i,
                'interval':interval,
                'bout_num':slice[slice['Start'] == interval[0]]['Bout'].iloc[0],
                'sex':slice[slice['Start'] == interval[0]]['Sex'].iloc[0],
                'strain':slice[slice['Start'] == interval[0]]['Strain'].iloc[0],
                'duration': slice.loc[(slice['Start'] >= interval[0]) & (slice['End'] <= interval[1]), 'Duration'].to_numpy()
            }

            toReturn.append(pull)

        return pd.DataFrame(toReturn)


    def multi_Vid_matchlog(self, vid_ind):
        '''
        Docstring for run_multiVid
        
        :param self: Description
        :param vid_ind: Description

        eventualy need support for strain, sex, others?
        '''
        pass

                







            


    
