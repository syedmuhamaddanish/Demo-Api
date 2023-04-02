from django.test import LiveServerTestCase, Client
from django.urls import reverse
from django.http import JsonResponse

class WhoMadeMeViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    # Tests for endpoint who-made-me
    def test_who_made_me(self):
        url = reverse('who-made-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {
            "Creator": "Syed Muhammad Danish",
            "FunFact": "I think I am a great cook"
        }
        self.assertDictEqual(response.json(), expected_data)
    
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'error': 'Method not allowed'}
        self.assertDictEqual(response.json(), expected_data)

    # Tests for endpoint number-to-word

    def test_number_to_word(self):
        response = self.client.post(reverse('number-to-word'), {'num': 2}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'word': 'two'}
        self.assertDictEqual(response.json(), expected_data)

        response = self.client.post(reverse('number-to-word'), {'num': '2'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'word': 'two'}
        self.assertDictEqual(response.json(), expected_data)

        response = self.client.post(reverse('number-to-word'), {'num': 10}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'error': 'Input must be an integer between 0 and 9'}
        self.assertDictEqual(response.json(), expected_data)

        response = self.client.post(reverse('number-to-word'), {'num': 'danish'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'error': 'Input must be an integer'}
        self.assertDictEqual(response.json(), expected_data)

        response = self.client.post(reverse('number-to-word'), {'not_num': 'abc'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'error': 'Input parameter missing'}
        self.assertDictEqual(response.json(), expected_data)

        response = self.client.post(reverse('number-to-word'), '{"foo": "bar",}', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        expected_data = {'error': 'Invalid JSON request body'}
        self.assertDictEqual(response.json(), expected_data)

    # Tests for endpoint get-word

    def test_get_word(self):
        response = self.client.get(reverse('get-word', args=['go']))
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('Example sentence', json_response.keys())

        response = self.client.get(reverse('get-word', args=['wallet']))
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('Dictionary definition', json_response.keys())

        response = self.client.get(reverse('get-word', args=['impeccable']))
        expected_response = {'result': 'Sorry, the word is neither a verb nor a noun'}
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertDictEqual(response.json(), expected_response)

        response = self.client.get(reverse('get-word', args=['defenestrate']))
        expected_response = {'result': 'This can be used as a verb, but unfortunately, there is no example available'}
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertDictEqual(response.json(), expected_response)

        response = self.client.get(reverse('get-word', args=[123]))
        expected_response = {'error': 'Input must be a word, not a number'}
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertDictEqual(response.json(), expected_response)

        # Test by inputting an English word which does not exists in the API. The
        # response by the API is generated as

        #{
        # "title":"No Definitions Found",
        # "message":"Sorry pal, we couldn't find definitions for the word you were looking for.",
        # "resolution":"You can try the search again at later time or head to the web instead."
        # }
        
        response = self.client.get(reverse('get-word', args=['asdfghytrwervsdfsdfsdf']))
        json_response = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('error', json_response.keys())

        response = self.client.post(reverse('get-word', args=['hello']))
        expected_response = {'error': 'Method not allowed'}
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, JsonResponse)
        self.assertDictEqual(response.json(), expected_response)


        # As certain verbs in the api do not have examples, there is a possiblity that
        # certain nouns might not have the definitions too although I did not find any noun.

        # This test is to check noun if the API provides its definition or not.
        
        # The test will not pass as I did not find any noun with no definition available.

        #response = self.client.get(reverse('get-word', args=['noun']))
        #expected_response = {'result': 'Sorry, No definition is available for this noun'}
        #self.assertEqual(response.status_code, 200)
        #self.assertIsInstance(response, JsonResponse)
        #self.assertDictEqual(response.json(), expected_response)