# Wrapify
<img width="150" align="center" alt="wrapify" src="https://github.com/user-attachments/assets/e6f5748c-434a-484d-813d-9b654d716ee3" /> A zotify wrapper to automatically iterate until all the songs in a &lt;spotify_url> are downloaded.

[Zotify](https://github.com/Googolplexed0/zotify) is cool and all, but librespot keeps failing a whole lot of times, meaning you will miss some files and need to restart zotify manually to complete the job. ***I need it to do it's thing unattended and that's what wrapify does.*** How so?

- we know how many songs we want to download
- we know where those files are going
- zotify automatically skips songs it downloaded already

Wrapify simply keeps calling zotify until the total number of songs was downloaded.

## Configuration
The idea is to tell wrapify how many files we want to download and which directory to watch for incoming files in order to determine wheter your downloads are complete. Zotify keeps track of the individual files itself, but in case it fails at some point for whatever reason, your downloads will be incomplete. In such a case wrapify will restart zotify (we call this 'taking another attempt') because it noticed that files are missing. Zotify will then automatically try to download them.

Consult your zotify config.json to figure out where the files are going. By default it will create subdirectories based on a template like this `{artist}/{album}/{album_num} - {artist} - {song_name}.{ext}`

You can tell wrapify to watch the subdirectories accordingly, or you can configure zotify to put all downloads into one single directory (i.e. without individual subdirectories for artists and albums). I do the latter and put all the files in `~/music/`, because it allows for easier bulk file editing afterwards.

## How to use it
It's very simple really:

`usage:   python wrapify.py <num_songs> <ext> <spotify_url> <download_dir>`

`example: python wrapify.py 42 ogg https://open.spotify.com/playlist/PLAYLIST_ID ~/Music/Zotify`

As of right now (June 2026) probably only [this fork of zotify](https://github.com/Googolplexed0/zotify) still works properly. So make sure to use that.

## What's the point
Why would you want to use a wrapper? Fork the damn thing and implement the missing functionality there ffs!

True. I might do that someday. For now this works alright.
