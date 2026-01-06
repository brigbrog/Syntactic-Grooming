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
import os

# create data set of input size with n target sequences

if __name__ == '__main__':

    # specify variables
    #length = input('length (int): ')
    target_seq = input('target sequence (string): ')
    n_seqs = input('number of target sequences (int): ')
    state_dur = input('state_duration (int): ')
    buffer_length = input('buffer length (int): ') 
    save_name = input('save name (string): ')

    # create output directory
    os.makedirs('./output')
    save_path = os.join('./output', save_name)

    # syntaxes
    syntaxes = ['Not_Grooming','Paw_Lick','Bilateral_Face_Wash','Genital_Groom','Flank_Lick','Unilateral_Face_Wash','Tail_Groom']

    # set start index
    start = 0

    fake_data_ls = []
    vid_len = len((target_seq * state_dur + buffer_length) * n_seqs)

    for i in range(n_seqs):
        buffer = {'Start' : start,
                'Duration': buffer_length,
                'State': 0,
                'Video_name': 'fake video',
                'NetworkFilename': 'fake file',
                'Strain': 'N/A',
                'Sex': 'N/A',
                'End': start + buffer_length,
                'Syntax': syntaxes[0],
                'Ordered_State': 0,
                'Bout': 'N/A',
                'Filtered_State': 0}
         
        # add buffer to data list
        fake_data_ls.append(buffer)

        # update start index
        start += buffer_length
        
        for j in target_seq:
            toAdd = {'Start' : start,
                    'Duration': state_dur,
                    'State': j,
                    'Video_name': 'fake video',
                    'NetworkFilename': 'fake file',
                    'Strain': 'N/A',
                    'Sex': 'N/A',
                    'End': start + state_dur,
                    'Syntax': syntaxes[int(j)],
                    'Ordered_State': j,
                    'Bout': 'N/A',
                    'Filtered_State': j}

            # add grooming to data list
            fake_data_ls.append(toAdd) 

            # update start index
            start += state_dur


    # Export CSV
    fake_data = pd.DataFrame(fake_data_ls)

    fake_data.to_csv(save_path, index=False)
    