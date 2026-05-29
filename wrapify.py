#!/usr/local/bin/python3
"""
Wrapify - A zotify wrapper to automatically iterate until all the songs in a <spotify_url> are downloaded.

May 2026 - D. Leicht
Copyright (c) 2026

This software is provided 'as-is', without any express or implied
warranty. In no event will the author be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.

Zotify @ https://github.com/zotify-dev/zotify
"""

import subprocess
import time
import os
import sys

# ─── Config ───────────────────────────────────────────────────────────────────
RETRY_DELAY  = 15
MAX_STALE    = 5
# ──────────────────────────────────────────────────────────────────────────────

def usage():
    print("usage:   python wrapify.py <num_songs> <ext> <spotify_url> <download_dir>")
    print("example: python wrapify.py 42 ogg https://open.spotify.com/playlist/PLAYLIST_ID ~/Music/Zotify")
    sys.exit(1)

if len(sys.argv) != 5:
    print(f"⚠️ Error: invalid number of parameters given.")
    usage()

try:
    total = int(sys.argv[1])
except ValueError:
    print(f"❌ Error: '{sys.argv[1]}' is not a valid number.")
    usage()

extensions = ["aac", "fdk_aac", "m4a", "mp3", "ogg", "opus", "vorbis"]
file_ext = sys.argv[2]
if file_ext not in extensions:
    print(f"❌ Error: invalid file extension given.\nValid options are {extensions}.\nFYI: you'll need ffmpeg for anything else than ogg.\n")
    usage()

spotify_url = sys.argv[3]
if "spotify.com" not in spotify_url:
    print(f"❌ Error: '{spotify_url}' doesn't look like a valid spotify_url.")
    usage()

download_dir = os.path.expanduser(sys.argv[4])
if not os.path.isdir(download_dir):
    print(f"⚠️ Caution: '{download_dir}' doesn't exist, yet. I will create it for you. Make sure zotify puts the files there (i.e. check your config.json).")
    try:
        os.mkdir(download_dir)
    except:
        print(f"❌ Error: Failed to create {download_dir}.")

def count_downloaded():
    return sum(1 for f in os.listdir(download_dir)
               if f.endswith(f".{file_ext}") and os.path.isfile(os.path.join(download_dir, f)))

# ─── Main ─────────────────────────────────────────────────────────────────────
print(f"Target: {total} songs | Playlist: {spotify_url} | Directory: {download_dir}\n")

attempt      = 0
stale_attempts = 0

while count_downloaded() < total:
    downloaded_before = count_downloaded()
    attempt += 1

    print(f"─── Attempt {attempt} | {downloaded_before}/{total} downloaded, {total - downloaded_before} missing ───\n")
    subprocess.run(["zotify", spotify_url])

    if count_downloaded() == downloaded_before:
        stale_attempts += 1
        print(f"\n⚠️ No progress ({stale_attempts}/{MAX_STALE})")
        if stale_attempts >= MAX_STALE:
            print(f"\n⚠️ Stopping the loop – no progress for {MAX_STALE} attempts. Please check the downloads manually.")
            sys.exit(1)
    else:
        stale_attempts = 0

    time.sleep(RETRY_DELAY)

print(f"\n✅ All {total} songs downloaded from {spotify_url}.")
sys.exit(0)