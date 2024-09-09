import unittest
from unittest.mock import patch, MagicMock
import torch
import json
import numpy as np
from models.chat import get_response, update_booking_data, extract_station_name, find_matching_stations, get_station_code


class TestChatFunctions(unittest.TestCase):

    @patch('models.chat.pymongo.MongoClient')
    @patch('models.chat.nlp')
    @patch('models.chat.PredictionBot')
    @patch('models.chat.TicketBot')
    @patch('models.chat.NeuralNet')
    @patch('models.chat.bag_of_words')
    @patch('models.chat.tokenize')
    @patch('models.chat.torch.load')
    @patch('models.chat.torch.max')
    @patch('models.chat.torch.softmax')
    def test_get_response_book(self, mock_softmax, mock_max, mock_load, mock_tokenize, mock_bag_of_words, mock_NeuralNet, mock_TicketBot, mock_PredictionBot, mock_nlp, mock_MongoClient):
        # Mock MongoDB client
        mock_MongoClient.return_value = MagicMock()

        # Mocking the tokenization and bag of words functions
        mock_tokenize.return_value = ['i', 'want', 'to', 'book', 'a', 'ticket']
        # Ensure this returns a NumPy array of the correct size
        mock_bag_of_words.return_value = np.zeros(61, dtype=np.float32)

        # Mocking the NeuralNet model
        mock_model = MagicMock()
        mock_NeuralNet.return_value = mock_model
        mock_model.eval.return_value = None
        mock_model.return_value = torch.Tensor([[0.1, 0.9]])

        # Mocking torch functions
        mock_max.return_value = (torch.Tensor([1]), torch.Tensor([1]))
        mock_softmax.return_value = torch.Tensor([[0.1, 0.9]])

        # Mocking json.load for intents
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = json.dumps({
            "intents": [
                {"tag": "book", "patterns": [], "responses": [
                    "Sure, I can help you book a ticket."]}
            ]
        })
        with patch('builtins.open', return_value=mock_file):
            response = get_response('I want to book a ticket')

        self.assertIn("Sure, I can help you book a ticket.", response)
        mock_TicketBot().reset.assert_called_once()

    @patch('models.chat.book_db')
    def test_update_booking_data(self, mock_book_db):
        booking = {
            'ticket_type': 'one way',
            'start_station': 'OXF',
            'destination_station': 'CMB',
            'departure_date': '2023-05-20',
            'departure_time': '10:00',
            'return_date': None,
            'return_time': None,
            'expecting': None
        }

        update_booking_data(booking)

        mock_book_db.update_one.assert_called_once_with(
            {"_id": 1},
            {"$set": {
                'ticket_type': 'one way',
                'start_station': 'OXF',
                'destination_station': 'CMB',
                'departure_date': '2023-05-20',
                'departure_time': '10:00'
            }},
            upsert=True
        )

    @patch('models.chat.nlp')
    def test_extract_station_name(self, mock_nlp):
        mock_doc = MagicMock()
        mock_nlp.return_value = mock_doc
        mock_doc.ents = [MagicMock(text='Oxford', label_='GPE')]

        station_name = extract_station_name(
            'I want to travel from Oxford to Cambridge')

        self.assertEqual(station_name, 'Oxford')

    @patch('models.chat.station_db')
    def test_find_matching_stations(self, mock_station_db):
        mock_station_db.find.return_value = [
            {'stationName': 'Oxford'}, {'stationName': 'Oxford Parkway'}]

        stations = find_matching_stations('Oxford')

        self.assertEqual(stations, ['Oxford', 'Oxford Parkway'])

    @patch('models.chat.station_db')
    def test_get_station_code(self, mock_station_db):
        mock_station_db.find_one.return_value = {'stationCode': 'OXF'}

        station_code = get_station_code('Oxford')

        self.assertEqual(station_code, 'OXF')


if __name__ == "__main__":
    unittest.main()
