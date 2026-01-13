import os
from FileCurtain import FileCurtain
from itertools import permutations

'''
Docstring for syntactic_grooming.target_generator

Creates a structured text file containing a list of 
target chains for use in BoutMachine identification.

Run from shell

inputs:
---------------------------------------------------
states: (string of integers) -> list of possible states for target creation
robust: (y/n) -> use all possible length of permutations
    lengths: if robust is 'n', input comma sep. lengths (int)
save_location: (fpath) -> name of file to save in output directory (auto)

output:
---------------------------------------------------
text file generation of all permutations specified under input params

NEED SUPPORT -> interruptions, incompletions

'''

def parse_lengths(length_in: str, split: str):

    strip_list = length_in.split(split)
    int_lengths = []

    for string in strip_list:
        intLen = int(string.strip())
        int_lengths.append(intLen)

    return int_lengths


## Permutations
def single_length_perm(states, length):
    # NEED non-adjacent combinations
    perms = permutations(states, r=length)
    return list(perms)

def varying_length_permutations(states, lengths: list = None):

    all_perms = []
    lengths = range(1, len(states)) if lengths == None else lengths

    for length in lengths:
        i_perms = single_length_perm(states, length)
        all_perms.extend(i_perms)

    return all_perms

def write_perms(save_name, perm_list):

    os.makedirs('../library/target_permutations', exist_ok = True)
    save_path = os.path.join('../library/target_permutations', save_name + '.txt')

    with open(save_path, 'w') as file:
        for perm in perm_list:
            file.writelines(perm)
            file.write('\n')
    print(f'Save to {save_path} complete.')


## ## ## ## ## ##

class Generator():
    def __init__(self):
        pass


    ## Interruptions
class Interruptions(Generator):
    def __init__(self, states):
        self.states = states

    def generate_inter(self, lengths):
        pass

    def verify_non_adj(self, prev_char, cur_char):
        pass

    def write(self, save_name):
        pass


    ## Incompletions
class Incompletions(Generator):
    def __init__(self, states):
        self.states = states

    def generate_incom(self, lengths):
        pass

    def verify_non_dec(self, prev_char, cur_char):
        pass

    def write(self, save_name):
        pass
    
class Permutations(Generator):
    def __init__(self, states: str, robust: bool, save_dir: str, save_name: str):
        self.states = states
        self.robust = robust
        self.save_dir = save_dir
        self.save_name = save_name
        self.perm_list = None

    def generate_perm(self, length):
        perms = permutations(self.states, r=length)
        return list(perms)
    
    def compile(self, lengths: list = None):
        self.perm_list = [] 
        lengths = range(1, len(self.states)) if lengths == None else lengths

        for length in lengths:
            i_perms = self.generate_perm(length)
            self.perm_list.extend(i_perms)

        return self.perm_list
    
    def write_perms(self):
        # Write file type options?
        libpath = os.path.join('../library', self.save_dir)
        os.makedirs(libpath, exist_ok = True)
        save_path = os.path.join(libpath, save_name + '.txt') 
        if self.perm_list is None or len(self.perm_list) == 0:
            raise ValueError('Permutations are None or empty')
        with open(save_path, 'w') as file:
            for perm in self.perm_list:
                file.writelines(perm)
                file.write('\n')
        print(f'Save to {save_path} complete.')




if __name__ == "__main__":
    
    # input
    states = input('Enter states (seq of ints): ')
    robust = input('Robust? (y/n): ').lower()
    lengths = parse_lengths(input('Perm lengths (comma seperated ints): '), ',') if robust == 'n' else None
    save = input('Save generation? (y/n): ')

    print(f'Generating permutations for states {states}, at {lengths if lengths != None else 'all'} lengths.')

    # run permutations
    perms = varying_length_permutations(states, lengths)

    print(f'{len(perms)} permutations created.')

    # save or print
    if save == 'y':
        save_name = input('Save fname: ')
        write_perms(save_name, perms)
    else:
        if input('Print permutations? (y/n): ').lower() == 'y':
            print(perms)

