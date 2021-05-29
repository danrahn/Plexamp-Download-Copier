from correlate import PlexampCorrelate
import os
import re
import shutil
import sys

class PlexampDownloadCopier:
    def __init__(self):
        self.correlator = PlexampCorrelate()
        self.savepath = ''
        self.get_savepath()
    def get_savepath(self):
        if self.savepath != '':
            return self.savepath
        savepath = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '-d' else input('Where would you like to copy your music to (full path)? ')
        while not os.path.exists(savepath) or not os.path.isdir(savepath):
            create = (f'{savepath} does not exist. Would you like to create it (y/n)? ')
            while create.lower()[0] not in ['y', 'n']:
                create = input(f'{savepath} does not exist. Would you like to create it (y/n)? ')
            if create[0].lower() == 'y':
                os.makedirs(savepath)
                break
            else:
                savepath = input('Where would you like to copy your music to (full path)? ')
        self.savepath = savepath
        return self.savepath
    
    def copy(self):
        files = self.correlator.correlate()
        for artist in files:
            for album in files[artist]:
                maxtrack = files[artist][album]['maxtrack']
                dst_dir = os.path.join(self.get_savepath(), artist, album)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                for src, track in files[artist][album]['tracks'].items():
                    filename = self.replace_invalid_characters(track["filename"])
                    dst_file = f'{self.pad_index(track["track_no"], len(str(maxtrack)))} - {filename}'
                    dst = os.path.join(dst_dir, dst_file)
                    if os.path.exists(dst):
                        print(f'WARN: {dst} exists! Not copying...')
                        continue
                    print(f'Copying \'{src}\' to \'{dst}\'')
                    try:
                        shutil.copy(src, dst)
                    except OSError as e:
                        print(f'Failed to copy {dst}: {e}')

    def pad_index(self, index, max):
        while len(index) < max:
            index = '0' + index
        return index
    
    def replace_invalid_characters(self, filename):
        """ Replaces invalid file name characters (<>:"/\|?*) with sensible alternatives"""
        filename = re.sub(r'[<>/\\|]', '-', filename) # For most invalid characters, replace with a dash
        filename = filename.replace(':', ' -') # Assume something like 'Song: Title', and change to 'Song - Title'
        filename = filename.replace('"', "'") # Replace double quotes with single quotes
        filename = re.sub(r'[?\*]', '', filename) # Just remove any asterisks or question marks
        return filename

if __name__ == '__main__':
    PlexampDownloadCopier().copy()