'''
Brian Brogan
Colby College - The Jackson Laboratory

3 November 2025
Synthetic Data Generator
------------------------
        This file is used to create synthetic training data for RNN implementations.
    The data should be used to develop and test RNNs for Syntactic Grooming chain
    analysis. The models created using this data serve as a proof of concept
    for categorical time series pattern recognition.

'''

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

class SyntheticGenerator():

    def __init__(self, syntaxes, pattern):
        '''Constructor for SyntheticGenerator class. Initializes the syntax categories 
        and ideal pattern sequence.

        Parameters:
        -----------
        syntaxes: array. Definitions of all possible syntaxes for time-series generation.
        pattern: array. Int-coded syntax sequence for basis of data.
        '''

        self.syntaxes = syntaxes
        self.pattern = pattern
    
    def generator(self, length: int, noise: float):
        pass


