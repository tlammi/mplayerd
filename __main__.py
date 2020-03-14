from mplayerd.media import MediaPlayer, Playlist
import time
import threading

FILES = [
    (r"C:\Users\Toni\Dropbox\Kuvat\JA7_2433.JPG", {"image-duration": "2.0"}),
    (r"C:\Users\Toni\Dropbox\Kuvat\JA7_2435.JPG", {"image-duration": "3.0"}),
    r"C:\Users\Toni\Dropbox\Puntti\nostot\ranking_1_2018_temppu_83.MP4"
]

FILES2 = [
    r"C:\Users\Toni\Dropbox\Puntti\nostot\ranking_1_2018_temppu_83.MP4"
]

plist = Playlist(FILES)
player = MediaPlayer(plist)


def thread(p: MediaPlayer):
    i = 0
    while True:
        if i % 2 == 0:
            p.playlist_replace(Playlist(FILES))
        else:
            p.playlist_replace(Playlist(FILES2))

        i += 1
        time.sleep(3)


t = threading.Thread(target=thread, args=(player,), daemon=True)
t.start()

player.run_forever()
