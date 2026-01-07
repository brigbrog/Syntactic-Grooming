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
    
    #def get_chain_acc(self, target_length):
    #    self.chain_acc = target_length

    def get_target_length(self):
        self.target_length = self.cur_video.shape[0]






    def read_state(self, reference):
        state_read = None
        if self.use_filt_state:
            state_read = reference['Filtered_State']
        else:
            state_read = reference['Ordered_State'] 

        return state_read
    

    def verify(self, state_read, target_chain, index):

        if state_read == target_chain[index]:
            return True
        
        return False



    def run_machine(self):
        #self.get_chain_acc()
        #self.chain_acc = 0
        # self.get_target_length() RUN INIT

        cur_start = 0
        cur_end = 0

        for idx, ref in enumerate(self.cur_video):
            
            # read the current state in the video
            state_read = self.read_state(ref)

            # verify if the read state agrees with current index of target chain (BOOL)
            if self.verify(state_read, self.target_chain, self.chain_acc):
                self.chain_acc += 1
                #cur_start = ref['Start']
                cur_start = idx
            else:
                self.chain_acc = 0

            # add bout to return field if chain accumulator reaches max

            if self.chain_acc == len(self.target_chain):
                pass
                



            # check if the current state is equal to the corresponding state in the target chain
            if state_read == self.target_chain[self.chain_acc]:

                # check if the chain_acc was previously 0, if yes record start
                if self.chain_acc == 0:
                    cur_start = ref['Start']
                    
                self.chain_acc += 1







            


    
