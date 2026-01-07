'''
Brian Brogan
Colby College - The Jackson Laboratory

3 December 2025
Grooming Bout Identifier (State Machine)
------------------------
'''

import numpy as np
import pandas as pd

class BoutMachine():

    def __init__(self,
                 data_fname: str,
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

        # load CSV video data
        self.load_df(data_fname)

    def load_df(self, fname):
        self.data = pd.read_csv(fname)

    def set_target_chain(self, target_chain: str):
        self.target_chain = target_chain

    def set_video(self, video: pd.DataFrame):
        self.cur_video = video

    def get_target_length(self):
        self.target_length = self.cur_video.shape[0]






    def read_state(self, reference):
        state_read = None
        if self.use_filt_state:
            state_read = int(reference['Filtered_State'])
        else:
            state_read = int(reference['Ordered_State'])

        return state_read
    

    def verify(self, state_read: int, target_chain, index):

        target = int(target_chain[index])

        if state_read == target:
            return True
        
        return False
    

    def run_machine(self, video: pd.DataFrame, verbose: bool = True):

        cur_start = np.nan
        cur_end = np.nan
        identified = 0
        log = {}

        for ref in video.iterrows():
            
            # read the current state in the video
            state_read = self.read_state(ref[1])

            if verbose:
                print(f'state read: {state_read} chain acc: {self.chain_acc} target val: {self.target_chain[self.chain_acc]} verify: {self.verify(state_read, self.target_chain, self.chain_acc)}')

            # verify if the read state agrees with current index of target chain (BOOL)
            if self.verify(state_read, self.target_chain, self.chain_acc):
                if self.chain_acc == 0:
                    cur_start = ref[1]['Start']
                self.chain_acc += 1

            # if not reset chain accumulator and start counter    
            else:
                self.chain_acc = 0
                cur_start = np.nan

            # add bout to return field if chain accumulator reaches max
            if self.chain_acc == len(self.target_chain):
                identified += 1
                cur_end = ref[1]['End']
                log[identified] = (cur_start, cur_end)

                # then reset chain accumulator and counters
                self.chain_acc = 0
                cur_start = np.nan
                cur_end = np.nan

        return log
                







            


    
