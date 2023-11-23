import unittest
from unittest.mock import patch
from extract_entities import extract_entities

class TestExtractEntities(unittest.TestCase):

    @patch('extract_entities.openai')
    def test_extract_entities_success(self, mock_openai):
        
        mock_response_success = {
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": {
                    "person": ["Jane Smith"],
                    "email": ["jane.smith@example.com"],
                    "phone_number": ["555-678-9012"],
                    "date": ["next Thursday"],
                    "time": ["3 PM"]
                },
            },
            "finish_reason": "stop"
        }],
    }

        mock_openai.ChatCompletion.create.return_value = mock_response_success
        
        result = extract_entities("Schedule a meeting with Jane Smith")
        self.assertIsInstance(result, dict)
        self.assertIn("person", result)
        self.assertEqual(result["person"], ["Jane Smith"])

    @patch('extract_entities.openai')
    def test_extract_entities_failure(self, mock_openai):
        mock_response_failure = {
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": {}
            },
            "finish_reason": "stop"
        }],
    }

        mock_openai.ChatCompletion.create.return_value = mock_response_failure
        
        result = extract_entities("some text with no entities")
        self.assertEqual(result, {})
