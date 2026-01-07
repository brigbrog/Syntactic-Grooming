'''
FileCurtain:
    Simple masking class for filepath hiding

    Library file structure ( for i files ):
    -----------------------
    Name_1
    fpath_1
    ...
    Name_i
    fpath_i
'''

class FileCurtain():

    def __init__(self, txt_path: str):
        self.txt_path = txt_path
        self.fpaths = {}
        self.populate_fpaths(self.txt_path)

    def populate_fpaths(self, txt_path):
        with open(txt_path, 'r') as library:
            lines = (line.strip() for line in library)

            for name, path in zip(lines, lines):
                self.fpaths[name] = path


if __name__ == '__main__':
    txt_path = input('enter library path (include .txt): ')

    fc = FileCurtain(txt_path)

    for i in fc.fpaths.keys():
        print(f'{i}: {fc.fpaths[i]}')