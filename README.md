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

## Usage

```
python plexampDownloadCopier.py [-d dir]

  -d dir - Full path to copy the music to. If not provided, the script will ask for a location.
```

## Notes

This script was made with Windows in mind, but technically should work with other OSs. The biggest downside is that this script won't automatically find the Plexamp download folder (on Windows, it's `%LOCALAPPDATA%\Plexamp\Plexamp\Offline`), and will instead interactively ask for its location.