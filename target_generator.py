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

'''


def single_length_perm(states, length):

    perms = permutations(states, r=length)
    return list(perms)

def varying_length_permutations(states, lengths: list = None):

    all_perms = []
    lengths = range(1, len(states)) if lengths == None else lengths

    for length in lengths:
        i_perms = single_length_perm(states, length)
        all_perms.extend(i_perms)

    return all_perms

def parse_lengths(length_in: str, split: str):

    strip_list = length_in.split(split)
    int_lengths = []

    for string in strip_list:
        intLen = int(string.strip())
        int_lengths.append(intLen)

    return int_lengths

def write_perms(save_name, perm_list):

    os.makedirs('./target_generator_output', exist_ok = True)
    save_path = os.path.join('./target_generator_output', save_name + '.txt')

    with open(save_path, 'w') as file:
        for perm in perm_list:
            file.writelines(perm)
            file.write('\n')


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

