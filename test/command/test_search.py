import os
import json
import re
import unittest
from darrcord import sonarr
from darrcord import radarr
from darrcord.command import search
from unittest.mock import PropertyMock, MagicMock, patch

tmdb_payload = os.path.join(os.path.dirname(__file__), 'tmdb_search_payload.json')

class TestSearchCommand(unittest.IsolatedAsyncioTestCase):
    test_channel = 'test_channel'

    def mock_message(self):
        msg = MagicMock()
        msg.channel = self.test_channel
        return msg

    #### handle_message ####

    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_no_results(self, mock_search_multi, mock_config):
        mock_search_multi.return_value = []
        reply = await search.handle_message('', self.mock_message())
        self.assertEqual(reply, {'content': 'No results.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_three_results(self, mock_search_multi, mock_config):
        result_count = 3

        with open(tmdb_payload) as f:
            tmdb_json = json.load(f)
        mock_search_multi.return_value = tmdb_json[:result_count]
        reply = await search.handle_message('', self.mock_message())

        expected_emojis = search.number_emojis[:result_count]
        for emoji in expected_emojis:
            self.assertRegex(reply['embed'].description, emoji)
        self.assertEqual(reply['reactions'], expected_emojis)


    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_full_results(self, mock_search_multi, mock_config):
        with open(tmdb_payload) as f:
            tmdb_json = json.load(f)
        mock_search_multi.return_value = tmdb_json
        reply = await search.handle_message('', self.mock_message())

        expected_emojis = search.number_emojis
        expected_result_count = len(expected_emojis)
        for emoji in expected_emojis:
            self.assertRegex(reply['embed'].description, emoji)
        self.assertEqual(reply['reactions'], expected_emojis)

    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_sonarr_channel(self, mock_search_multi, mock_config):
        mock_search_multi.return_value = []
        type(mock_config).SONARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        reply = await search.handle_message('', self.mock_message())
        mock_search_multi.assert_called_with('', ['tv'])

    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_radarr_channel(self, mock_search_multi, mock_config):
        mock_search_multi.return_value = []
        type(mock_config).RADARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        reply = await search.handle_message('', self.mock_message())
        mock_search_multi.assert_called_with('', ['movie'])

    @patch('darrcord.command.search.Config')
    @patch('darrcord.tmdb.search_multi', autospec=True)
    async def test_handle_message_radarr_and_sonarr_channel(self, mock_search_multi, mock_config):
        mock_search_multi.return_value = []
        type(mock_config).SONARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        type(mock_config).RADARR_CHANNELS = PropertyMock(return_value=[ self.test_channel ])
        reply = await search.handle_message('', self.mock_message())
        mock_search_multi.assert_called_with('', ['tv', 'movie'])


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
    async def test_handle_reaction_radarr(self, mock_request_command, mock_config):
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_embed = MagicMock()
        mock_user.id = self.sample_user_id
        mock_embed.description = self.sample_message
        mock_reaction.__str__.return_value = "1️⃣"
        mock_reaction.message.embeds = [ mock_embed ]
        reply = await search.handle_reaction(mock_reaction, mock_user)
        mock_request_command.assert_called_with("tmdb:11", None, title='Star Wars (1977)')


    @patch('darrcord.command.search.Config')
    @patch('darrcord.command.request.handle_message', autospec=True)
    async def test_handle_reaction_sonarr(self, mock_request_command, mock_config):
        mock_reaction = MagicMock()
        mock_user = MagicMock()
        mock_embed = MagicMock()
        mock_user.id = self.sample_user_id
        mock_embed.description = self.sample_message
        mock_reaction.__str__.return_value = "2️⃣"
        mock_reaction.message.embeds = [ mock_embed ]
        reply = await search.handle_reaction(mock_reaction, mock_user)
        mock_request_command.assert_called_with("tmdb:181812", None, title='Star Wars: The Rise of Skywalker (2019)')

if __name__ == '__main__':
    unittest.main()
