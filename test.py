from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Set up before tests"""
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_main(self):
        """check thhat the board is in, that highscore is 0 , that nplays is 0, that html loads """
        with self.client:
            response = self.client.get('/')
            self.assertIn('board',session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'Score:',response.data)
    
    def test_not_real_word(self):
        """Test a word that doesnt exist"""

        self.client.get('/')
        response = self.client.get(
            '/guess?word=fakjjkdadjadkjadjkajkajkad')
        self.assertEqual(response.json['result'], 'not-word')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        self.client.get('/')
        response = self.client.get('/guess?word=adrianits')
        self.assertEqual(response.json['result'], 'not-on-board')
    
    def test_valid_word(self):
        """Test if word is valid"""
        with self.client as client:
            with client.session_transaction() as sesh:
                sesh['board'] = [["A", "D", "A", "P", "T"], 
                                 ["A", "D", "A", "P", "T"], 
                                 ["A", "D", "A", "P", "T"], 
                                 ["A", "D", "A", "P", "T"], 
                                 ["A", "D", "A", "P", "T"]]
        response = self.client.get('/guess?word=adapt')
        self.assertEqual(response.json['result'], 'ok')

