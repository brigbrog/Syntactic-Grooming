'''creates fake dataset for bout machine testing

Syntax encoding:

    Not_Grooming : 0
    Paw_Lick : 1
    Bilateral_Face_Wash : 2
    Genital_Groom : 5
    Flank_Lick : 4
    Unilateral_Face_Wash : 3
    Tail_Groom : 6

'''

import pandas as pd
import numpy as np

# create data set of input size with n target sequences

if __name__ == '__main__':

    # specify variables
    #length = input('length (int): ')
    target_seq = input('target sequence (string): ')
    n_seqs = input('number of target sequences (int): ')
    state_dur = input('state_duration (int): ')
    buffer_length = input('buffer length (int): ') 
    save_name = input('save name (string): ')

    # syntaxes
    syntaxes = ['Not_Grooming','Paw_Lick','Bilateral_Face_Wash','Genital_Groom','Flank_Lick','Unilateral_Face_Wash','Tail_Groom']

    # create dataframe

    #fake_data = pd.Dataframe(columns=['Start','Duration','State','Video_name','NetworkFilename','Strain','Sex','End','Syntax','Ordered_State','Bout','Filtered_State'])

    fake_data_ls = []
    vid_len = len((target_seq * state_dur + buffer_length) * n_seqs)

    for i in range(n_seqs):
        buffer = {'Start' : i + state_dur,
                'Duration': buffer_length,
                'State': 0,
                'Video_name': 'fake video',
                'NetworkFilename': 'fake file',
                'Strain': 'N/A',
                'Sex': 'N/A',
                'End': i + buffer_length,
                'Syntax': syntaxes[int(j)],
                'Ordered_State': 0,
                'Bout': 'N/A',
                'Filtered_State': 0}
        
        fake_data_ls.append(buffer)
        
        for j in target_seq:

            toAdd = {'Start' : i,
                    'Duration': state_dur,
                    'State': j,
                    'Video_name': 'fake video',
                    'NetworkFilename': 'fake file',
                    'Strain': 'N/A',
                    'Sex': 'N/A',
                    'End': i + state_dur,
                    'Syntax': syntaxes[int(j)],
                    'Ordered_State': j,
                    'Bout': 'N/A',
                    'Filtered_State': j}

            fake_data_ls.append(toAdd) 

    fake_data = pd.DataFrame(fake_data_ls)

    