import json
import platform
import os

class PlexampCorrelate:
    def __init__(self):
        self.appdir = ''
        self.get_app_dir()

    def get_app_dir(self):
        if self.appdir != '':
            return self.appdir
        expected = ""
        system = platform.system().lower()
        if system == 'windows' and 'LOCALAPPDATA' in os.environ:
            expected = os.path.join(os.environ['LOCALAPPDATA'], 'Plexamp', 'Plexamp', 'Offline')
        elif system == 'darwin' and 'HOME' in os.environ:
            expected = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'Plexamp', 'Offline')
        elif system == 'linux' and 'HOME' in os.environ:
            expected = os.path.join(os.environ['HOME'], '.local', 'share', 'Plexamp', 'Offline')
        if len(expected) > 0 and os.path.exists(expected):
                self.appdir = expected
                return self.appdir
        appdir = input('Could not find default PlexAmp download directory. Please enter the full path to the "Offline" folder:\n>')
        while not os.path.exists(appdir):
            appdir = input('That directory does not exist. Please enter the full path: ')
        self.appdir = appdir
        return self.appdir

    def correlate(self):
        appdir = self.get_app_dir()
        files = {}
        for subdir in os.listdir(appdir):
            fullpath = os.path.join(appdir, subdir)
            if not os.path.isdir(fullpath):
                continue # We expect the root download folder to only contain other folders
            mapfile = os.path.join(fullpath, 'index.json')
            if not os.path.exists(mapfile):
                print(f'ERROR: Could not find expected index.json file, skipping {subdir}')
            try:
                with open(mapfile, encoding='utf-8') as j:
                    index = json.load(j)
            except Exception:
                print(f'ERROR: Could not read index.json for {subdir}, skipping...')
                continue
            for item in index['items']:
                # For file/folder names, don't use the 'fancy' apostrophe
                artist = self.keyOrDefault(item, 'grandparentTitle', 'Unknown Artist').replace('\u2019', "'")
                album = self.keyOrDefault(item, 'parentTitle', 'Unknown Album').replace('\u2019', "'")
                track = self.keyOrDefault(item, 'title', 'Unknown Track').replace('\u2019', "'")
                track_no = self.keyOrDefault(item, 'index', 1) # Make all unspecified tracks track 1
                if artist not in files:
                    files[artist] = {}
                if album not in files[artist]:
                    files[artist][album] = { 'maxtrack' : 0, 'tracks' : {} }
                files[artist][album]['tracks'][os.path.join(fullpath, item['guid'])] = {
                    'track_no' : str(track_no),
                    'filename' : track + os.path.splitext(item['media'][0]['parts'][0]['key'])[1]
                }

                files[artist][album]['maxtrack'] = max(files[artist][album]['maxtrack'], track_no)
        return files

    def keyOrDefault(self, item, key, default):
        if key in item:
            return item[key]
        print(f'WARN: Could not find \'{key}\' for the current track, defaulting to \'{default}\'')
        return default
