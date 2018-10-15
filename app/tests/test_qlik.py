import os
import unittest
import json

from app import app, db




class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_check_palindrome_true(self):
        add_response = self.app.post('/add/', data=json.dumps(dict(value='racecar')), content_type='application/json')
        if not self.assertEqual(add_response.status_code, 201):
            return False
        response = self.app.post('/check/', data=json.dumps(dict(message_id='1')), content_type='application/json')
        self.assertEqual(response.status_code, 200) and self.assertEqual(response.json["palindrome"], 1)

    def test_check_palindrome_false(self):
        add_response = self.app.post('/add/', data=json.dumps(dict(value='helloworld')), content_type='application/json')
        if not self.assertEqual(add_response.status_code, 201):
            return False
        response = self.app.post('/check/', data=json.dumps(dict(message_id='1')), content_type='application/json')
        self.assertEqual(response.status_code, 200) and self.assertEqual(response.json["palindrome"], 0)

    def test_add_bad_request(self):
        add_response = self.app.post('/add/', data=json.dumps(dict(value='helloworld!')), content_type='application/json')
        self.assertEqual(add_response.status_code, 400)

    def test_delete(self):
        add_response = self.app.post('/add/', data=json.dumps(dict(value='racecar')), content_type='application/json')
        if not self.assertEqual(add_response.status_code, 201):
            return False
        response = self.app.delete('/delete/', data=json.dumps(dict(message_id='1')), content_type='application/json')
        self.assertEqual(response.status_code, 200)




if __name__ == "__main__":
    unittest.main()