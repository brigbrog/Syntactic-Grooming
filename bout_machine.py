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
    
    #def get_chain_acc(self, target_length):
    #    self.chain_acc = target_length

    def get_target_length(self):
        self.target_length = self.cur_video.shape[0]

    def run_machine(self):
        #self.get_chain_acc()
        self.chain_acc = 0
        self.get_target_length()

        cur_start = 0

        for idx, ref in enumerate(self.cur_video):
            if self.phase == 0:
                # read the current grooming state in the video
                if self.use_filt_state:
                    state_read = ref['Filtered_State']
                else: 
                    state_read = ref['Ordered_State']
                
            # check if the current state is equal to the corresponding state in the target chain
            if state_read == self.target_chain[self.chain_acc]:

                # check if the chain_acc was previously 0, if yes record start
                if self.chain_acc == 0:
                    cur_start = ref['Start']
                    
                self.chain_acc += 1







            


    
