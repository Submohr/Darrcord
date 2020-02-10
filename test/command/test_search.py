import os
import json
import re
import unittest
from darrcord import sonarr
from darrcord import radarr
from darrcord.command import search
from unittest.mock import PropertyMock, MagicMock, patch

sonarr_payload = os.path.join(os.path.dirname(__file__), 'sonarr_search_payload.json')
radarr_payload = os.path.join(os.path.dirname(__file__), 'radarr_search_payload.json')

class TestSearchCommand(unittest.TestCase):
    test_channel = 'test_channel'

    def mock_message(self):
        msg = MagicMock()
        msg.channel = self.test_channel
        return msg

    #### handle_message ####

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_no_results(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        mock_req_series_lookup.return_value = { "json": [] }
        mock_req_movie_lookup.return_value = { "json": [] }
        reply = search.handle_message('', self.mock_message())
        self.assertEqual(reply, {'content': 'No results.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_three_results(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        result_count = 3

        with open(sonarr_payload) as f:
            sonarr_json = json.load(f)
        mock_req_series_lookup.return_value = { "json": sonarr_json[:result_count] }
        mock_req_movie_lookup.return_value = { "json": [] }
        reply = search.handle_message('', self.mock_message())

        expected_emojis = search.number_emojis[:result_count]
        for emoji in expected_emojis:
            self.assertRegex(reply['embed'].description, emoji)
        self.assertEqual(reply['reactions'], expected_emojis)

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_full_results(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        with open(sonarr_payload) as f:
            sonarr_json = json.load(f)
        with open(radarr_payload) as f:
            radarr_json = json.load(f)
        mock_req_series_lookup.return_value = { "json": sonarr_json }
        mock_req_movie_lookup.return_value = { "json": radarr_json }
        reply = search.handle_message('', self.mock_message())

        expected_emojis = search.number_emojis
        expected_result_count = len(expected_emojis)
        for emoji in expected_emojis:
            self.assertRegex(reply['embed'].description, emoji)
        self.assertEqual(reply['reactions'], expected_emojis)

        radarr_links = re.findall(re.escape(radarr.tmdb_url), reply['embed'].description)
        sonarr_links = re.findall(re.escape(sonarr.tvdb_url), reply['embed'].description)
        self.assertEqual(len(radarr_links), expected_result_count / 2, msg="Expected half of the results to be from radarr")
        self.assertEqual(len(sonarr_links), expected_result_count / 2, msg="Expected half of the results to be from sonarr")

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_sonarr_channel(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        test_channel = 'test_channel'
        type(mock_config).SONARR_CHANNELS = PropertyMock(return_value=[ test_channel ])
        mock_req_series_lookup.return_value = { "json": [] }
        mock_req_movie_lookup.return_value = { "json": [] }
        reply = search.handle_message('', self.mock_message())
        self.assertTrue(mock_req_series_lookup.called)
        self.assertFalse(mock_req_movie_lookup.called)

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_radarr_channel(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        test_channel = 'test_channel'
        type(mock_config).RADARR_CHANNELS = PropertyMock(return_value=[ test_channel ])
        mock_req_series_lookup.return_value = { "json": [] }
        mock_req_movie_lookup.return_value = { "json": [] }
        reply = search.handle_message('', self.mock_message())
        self.assertFalse(mock_req_series_lookup.called)
        self.assertTrue(mock_req_movie_lookup.called)

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_lookup', autospec=True)
    @patch('darrcord.sonarr.req_series_lookup', autospec=True)
    def test_handle_message_radarr_and_sonarr_channel(self, mock_req_series_lookup, mock_req_movie_lookup, mock_config):
        type(mock_config).SONARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        type(mock_config).RADARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        mock_req_series_lookup.return_value = { "json": [] }
        mock_req_movie_lookup.return_value = { "json": [] }
        reply = search.handle_message('', self.mock_message())
        self.assertTrue(mock_req_series_lookup.called)
        self.assertTrue(mock_req_movie_lookup.called)


    #### handle_reaction ####

    sample_message = ("Here's what I found, <@1234>. Click a number to select one."
            "1️⃣ [Star Wars (1977)](https://www.themoviedb.org/movie/11)"
            "2️⃣ [Star Wars: Forces of Destiny (2017)](https://www.thetvdb.com/?tab=series&id=330710)"
            "3️⃣ [Star Wars: The Rise of Skywalker (2019)](https://www.themoviedb.org/movie/181812)"
            "4️⃣ [Star Wars: Go Rogue (2016)](https://www.thetvdb.com/?tab=series&id=358145)"
            "5️⃣ [Star Wars: The Force Awakens (2015)](https://www.themoviedb.org/movie/140607)"
            "6️⃣ [Star Wars: The Clone Wars (2008)](https://www.thetvdb.com/?tab=series&id=83268)")
    sample_user_id = '1234'

    @patch('darrcord.command.search.Config')
    @patch('darrcord.command.request.handle_message', autospec=True)
    def test_handle_reaction_radarr(self, mock_request_command, mock_config):
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_embed = MagicMock()
        mock_user.id = self.sample_user_id
        mock_embed.description = self.sample_message
        mock_reaction.__str__.return_value = "1️⃣"
        mock_reaction.message.embeds = [ mock_embed ]
        reply = search.handle_reaction(mock_reaction, mock_user)
        mock_request_command.assert_called_with("tmdb:11", None)


    @patch('darrcord.command.search.Config')
    @patch('darrcord.command.request.handle_message', autospec=True)
    def test_handle_reaction_sonarr(self, mock_request_command, mock_config):
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_embed = MagicMock()
        mock_user.id = self.sample_user_id
        mock_embed.description = self.sample_message
        mock_reaction.__str__.return_value = "2️⃣"
        mock_reaction.message.embeds = [ mock_embed ]
        reply = search.handle_reaction(mock_reaction, mock_user)
        mock_request_command.assert_called_with("tmdb:181812", None)

if __name__ == '__main__':
    unittest.main()