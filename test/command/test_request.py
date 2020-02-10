import os
import json
import unittest
from darrcord.command import request
from unittest.mock import patch

sonarr_payload = os.path.join(os.path.dirname(__file__), 'sonarr_request_payload.json')
sonarr_error_payload = os.path.join(os.path.dirname(__file__), 'sonarr_request_payload_error.json')
radarr_payload = os.path.join(os.path.dirname(__file__), 'radarr_request_payload.json')
radarr_error_payload = os.path.join(os.path.dirname(__file__), 'radarr_request_payload_error.json')

class TestRequestCommand(unittest.TestCase):
    #### handle_message ####

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_sonarr_empty_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        mock_req_series_request.return_value = { "code": 0, "json": None }
        reply = request.handle_message('tvdb:0', None)
        self.assertEqual(reply, {'content': 'Unknown error.  No error message.  Sorry.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_sonarr_error_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        with open(sonarr_error_payload) as f:
            sonarr_json = json.load(f)
        mock_req_series_request.return_value = { "code": 400, "json": sonarr_json }
        reply = request.handle_message('tvdb:0', None)
        self.assertEqual(reply, {'content': 'Error adding series.  Error message is: This series has already been added.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_sonarr_normal_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        with open(sonarr_payload) as f:
            sonarr_json = json.load(f)
        mock_req_series_request.return_value = { "code": 200, "json": sonarr_json }
        reply = request.handle_message('tvdb:0', None)
        self.assertEqual(reply, {'content': 'Successfully requested Star Trek: Picard: https://www.thetvdb.com/?tab=series&id=0'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_radarr_empty_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        mock_req_movie_request.return_value = { "code": 0, "json": None }
        reply = request.handle_message('tmdb:0', None)
        self.assertEqual(reply, {'content': 'Unknown error.  No error message.  Sorry.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_radarr_error_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        with open(radarr_error_payload) as f:
            radarr_json = json.load(f)
        mock_req_movie_request.return_value = { "code": 400, "json": radarr_json }
        reply = request.handle_message('tmdb:0', None)
        self.assertEqual(reply, {'content': 'Error adding movie.  Error message is: This movie has already been added.'})

    @patch('darrcord.command.search.Config')
    @patch('darrcord.radarr.req_movie_request', autospec=True)
    @patch('darrcord.sonarr.req_series_request', autospec=True)
    def test_handle_message_radarr_normal_response(self, mock_req_series_request, mock_req_movie_request, mock_config):
        with open(radarr_payload) as f:
            radarr_json = json.load(f)
        mock_req_movie_request.return_value = { "code": 200, "json": radarr_json }
        reply = request.handle_message('tmdb:0', None)
        self.assertEqual(reply, {'content': 'Successfully requested Star Wars: https://www.themoviedb.org/movie/0'})


if __name__ == '__main__':
    unittest.main()