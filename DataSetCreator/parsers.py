class EchoNestParser:
    @staticmethod
    def update(json_data):
        """
        Updates the json with all EchoNest data available for this song
        :param json_data: json object to update """
        pass


class LastFMParser:
    @staticmethod
    def update(json_data):
        """
        Updates the json with all Last.FM data available for this song
        :param json_data: json object to update """
        pass


class LyricsParser:
    @staticmethod
    def update(json_data):
        """
        TODO: update the json_data object with lyrics
        something like this:
        json_data[...] = get_lyrics(json_data['id'])
        :param json_data: json object to update """
        pass
