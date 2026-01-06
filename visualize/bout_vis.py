import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

def vid_compare(df: pd.DataFrame, vid_ids: list, plot_size: tuple = None):
    "Displays syntax classifications for specified sequence of videos drawn from dataframe in plot array."

    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(df['Video_name'].copy())
    le_syn_vec = sle.fit_transform(df['Syntax'].copy())

    #vid_ids_bvec = np.isin(le_vid_vec, vid_ids).astype(int)

    #sub_df = df.iloc[vid_ids_bvec, :]
    #le_syn_vec = sle.fit_transorm(df['Syntax'].copy())

    fig, axes = plt.subplots(len(vid_ids), 1, figsize=(25, 4*len(vid_ids)))
    plt.rcParams.update({'font.size': 16})

    for idx, vid_id in enumerate(vid_ids):
        x = np.linspace(0, le_syn_vec[le_vid_vec == vid_id].shape[0], le_syn_vec[le_vid_vec == vid_id].shape[0])
        axes[idx].plot(x, le_syn_vec[le_vid_vec == vid_id])

        axes[idx].set_title(f'Video # {vid_id}')
        axes[idx].set_yticks(np.arange(0, 7))

        fig.supxlabel("Frame Index")
        fig.supylabel("Grooming States")

    plt.tight_layout()
    plt.show()


def vid_ordstate_view_w_time(vid_df, vid_ids, plot_sz=None):
    fig, axes = plt.subplots(len(vid_ids), 1, figsize=(25, 4*len(vid_ids)))
    plt.rcParams.update({'font.size': 16})

    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    for idx, vid_id in enumerate(vid_ids):

        cur_vid = vid_df.loc[le_vid_vec == vid_id, :]

        t_min = np.min(cur_vid.loc[:, 'Start'])
        t_max = np.max(cur_vid.loc[:, 'End'])

        x = np.linspace(0, t_max-t_min, t_max-t_min)
        y = np.zeros((t_max-t_min,))
        for i in range(len(cur_vid)):
            cur_bout = cur_vid.iloc[i, :]
            strt = cur_bout['Start']
            dur = cur_bout['Duration']
            state = cur_bout['Ordered_State']

            y[strt:strt+dur] = state

        axes[idx].plot(x, y)
        axes[idx].set_title(f'Video # {vid_id}')
        axes[idx].set_yticks(np.arange(0, 7))

        fig.supxlabel("Frame Index")
        fig.supylabel("Grooming States")
    
def vid_filtstate_view_w_time(vid_df, vid_ids, plot_sz=None):
    fig, axes = plt.subplots(len(vid_ids), 1, figsize=(25, 4*len(vid_ids)))
    plt.rcParams.update({'font.size': 16})

    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    for idx, vid_id in enumerate(vid_ids):

        cur_vid = vid_df.loc[le_vid_vec == vid_id, :]
        t_min = np.min(cur_vid.loc[:, 'Start'])
        t_max = np.max(cur_vid.loc[:, 'End'])

        x = np.linspace(0, t_max-t_min, t_max-t_min)
        y = np.zeros((t_max-t_min,))
        for i in range(len(cur_vid)):
            cur_bout = cur_vid.iloc[i, :]
            strt = cur_bout['Start']
            dur = cur_bout['Duration']
            if cur_bout['Filtered_State'] == 'X':
                state = 0
            else:
                state = cur_bout['Filtered_State']
            

            y[strt:strt+dur] = state

        axes[idx].plot(x, y)
        axes[idx].set_title(f'Video # {vid_id}')
        axes[idx].set_yticks(np.arange(0, 7))

        fig.supxlabel("Frame Index")
        fig.supylabel("Grooming States")


def manual_inspect_ordstate(vid_df, vid_id: int, window: tuple):
    ''''''
    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    vid = vid_df.loc[le_vid_vec == vid_id, :]

    t_min = np.min(vid.loc[:, 'Start'])
    t_max = np.max(vid.loc[:, 'End'])
    y = np.zeros((t_max-t_min,))

    for i in range(len(vid)):
        cur_bout = vid.iloc[i, :]
        strt = cur_bout['Start']
        dur = cur_bout['Duration']
        state = cur_bout['Ordered_State']
        y[strt:strt+dur] = state

    y_view = y[window[0]:window[1]]
    x = np.linspace(window[0], window[1], y_view.shape[0])

    plt.title(f'Vid # {vid_id}')
    plt.xlabel(f'Frame Slice')
    plt.ylabel(f'Grooming State')

    plt.plot(x, y_view)
    plt.show()
    

def manual_inspect_filtstate(vid_df, vid_id: int, window: tuple, fig_sz=None):
    ''''''
    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    vid = vid_df.loc[le_vid_vec == vid_id, :]

    t_min = np.min(vid.loc[:, 'Start'])
    t_max = np.max(vid.loc[:, 'End'])
    y = np.zeros((t_max-t_min,))

    for i in range(len(vid)):
        cur_bout = vid.iloc[i, :]
        strt = cur_bout['Start']
        dur = cur_bout['Duration']
        if cur_bout['Filtered_State'] == 'X':
                state = 0
        else:
            state = cur_bout['Filtered_State']
        y[strt:strt+dur] = state

    y_view = y[window[0]:window[1]]
    x = np.linspace(window[0], window[1], y_view.shape[0])

    if fig_sz == None:
        fig_sz = (5, 5)

    plt.figure(figsize=fig_sz) 

    plt.title(f'Vid # {vid_id}')
    plt.xlabel(f'Frame Slice')
    plt.ylabel(f'Grooming State')

    plt.plot(x, y_view)
    plt.show()

def rost_caud_simplify(state):
    if state <= 2 and state > 0:
        return 1
    elif state >= 3:
        return 2
    else:
        return 0

def rost_caud_filtstate_view(vid_df, vid_ids, plot_sz=None):
    fig, axes = plt.subplots(len(vid_ids), 1, figsize=(25, 4*len(vid_ids)))
    plt.rcParams.update({'font.size': 16})

    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    for idx, vid_id in enumerate(vid_ids):

        cur_vid = vid_df.loc[le_vid_vec == vid_id, :]
        t_min = np.min(cur_vid.loc[:, 'Start'])
        t_max = np.max(cur_vid.loc[:, 'End'])

        x = np.linspace(0, t_max-t_min, t_max-t_min)
        y = np.zeros((t_max-t_min,))
        for i in range(len(cur_vid)):
            cur_bout = cur_vid.iloc[i, :]
            strt = cur_bout['Start']
            dur = cur_bout['Duration']
            if cur_bout['Filtered_State'] == 'X':
                state = 0
            else:
                state = cur_bout['Filtered_State']
            
            
            new = rost_caud_simplify(int(state))

            y[strt:strt+dur] = new

        axes[idx].plot(x, y)
        axes[idx].set_title(f'Video # {vid_id}')
        axes[idx].set_yticks(np.arange(0, 3))

        fig.supxlabel("Frame Index")
        fig.supylabel("Grooming States")

def manual_inspect_rost_caud_filtstate(vid_df, vid_id: int, window: tuple, fig_sz=None):
    ''''''
    sle = sklearn.preprocessing.LabelEncoder()
    le_vid_vec = sle.fit_transform(vid_df['Video_name'].copy())

    vid = vid_df.loc[le_vid_vec == vid_id, :]

    t_min = np.min(vid.loc[:, 'Start'])
    t_max = np.max(vid.loc[:, 'End'])
    y = np.zeros((t_max-t_min,))

    for i in range(len(vid)):
        cur_bout = vid.iloc[i, :]
        strt = cur_bout['Start']
        dur = cur_bout['Duration']
        if cur_bout['Filtered_State'] == 'X':
                state = 0
        else:
            state = cur_bout['Filtered_State']
        new = rost_caud_simplify(int(state))

        y[strt:strt+dur] = new

    y_view = y[window[0]:window[1]]
    x = np.linspace(window[0], window[1], y_view.shape[0])

    if fig_sz == None:
        fig_sz = (5, 5)

    plt.figure(figsize=fig_sz) 

    plt.title(f'Vid # {vid_id} (ceph/caud)')
    plt.xlabel(f'Frame Slice')
    plt.yticks([0, 1, 2])
    plt.ylabel(f'Grooming State')

    plt.plot(x, y_view)
    plt.show()

def inspect_bout():
    pass 