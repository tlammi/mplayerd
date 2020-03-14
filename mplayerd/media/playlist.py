from . import media


class Playlist:

    def __init__(self, medialist: list):
        self._media = []
        for m in medialist:
            if isinstance(m, media.Media):
                self._media.append(m)
            elif isinstance(m, str):
                self._media.append(media.Media(m))
            else:
                self._media.append(media.Media(*m))

        self._index = 0
        self._iter = None

    def append(self, newmedia):
        if isinstance(newmedia, media.Media):
            self._media.append(newmedia)
        else:
            self._media.append(media.Media(*newmedia))

    def __getitem__(self, item: int):
        return self._media[item]

    def __len__(self):
        return len(self._media)
