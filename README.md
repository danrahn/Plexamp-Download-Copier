# Plexamp Download Copier

This script copies downloaded music from Plexamp to a location of your choice.

When you download music in plexamp, it is given a random guid as a filename with no extension, making it impossible to know at a glance what each file corresponds to. However, each download folder also includes an `index.json` that contains the metadata for all the items, which can be used to correlate the guid to the right track.

After correlating each file to its underlying track, the script will copy them to a new location with the following hierarchy:

```
Root\
  Artist1\
    Album1\
      01 - Track1.mp3
      02 - Track2.m4a
    Album2\
  Artist2\
    Album1\
  ...
```

## Requirements

Python 3. If running `python` defaults to Python 2, use `python3` or `py -3` (depending on your platform) to invoke the script instead.

## Usage

```
python plexampDownloadCopier.py [-d dir]

  -d dir - Full path to copy the music to. If not provided, the script will ask for a location. If the path does not exist, the script will ask before creating it.
```

## Notes

This script was tested on Windows and Ubuntu, but should work on other platforms. Regardless, the worst that should happen is the script not automatically finding the PlexAmp download directory, in which case it will interactively ask the user to supply that location.
