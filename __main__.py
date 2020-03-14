from mplayerd.media import MediaPlayer, Playlist

FILES = [
    (r"C:\Users\Toni\Dropbox\Kuvat\JA7_2433.JPG", {"image-duration": "2.0"}),
    (r"C:\Users\Toni\Dropbox\Kuvat\JA7_2435.JPG", {"image-duration": "3.0"}),
    r"C:\Users\Toni\Dropbox\Puntti\nostot\ranking_1_2018_temppu_83.MP4"
]

plist = Playlist(FILES)
player = MediaPlayer(plist)
i = 0


player.run_forever()
