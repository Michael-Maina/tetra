import pytest
import time
from io import BytesIO
from flask_testing import TestCase
from unittest.mock import patch
from app import create_app
from views import extracted_data_storage, cleanup_extracted_data

class TestViews(TestCase):
    
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app
    
    @patch('views.transcribe_audio')
    @patch('views.extract_entities')
    def test_handle_audio(self, mock_extract,mock_transcribe):
        mock_audio = BytesIO(b"fake audio data")
        mock_audio.name = 'test_audio.wav'
        mock_transcribe.return_value = "call Jane Smith"
        mock_extract.return_value = {"person": ["Jane Smith"]}
        
        data = {'audio': (mock_audio, 'test_audio.wav')} 
        response = self.client.post('/audios', content_type='multipart/form-data', data=data)
        
        mock_audio.close()
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("transcription_text", response.json)
        self.assertIn("data_key", response.json)
        self.assertEqual(response.json["transcription_text"], "call Jane Smith")
        mock_transcribe.assert_called_once()
        mock_extract.assert_called_once_with("call Jane Smith")
  
    def test_handle_audio_invalid_file_type(self):
        mock_audio = BytesIO(b"not an audio file")
        mock_audio.name = 'invalid_file.txt'

        data = {'audio': (mock_audio, 'invalid_file.txt')} 
        response = self.client.post('/audios', content_type='multipart/form-data', data=data)

        mock_audio.close()
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid file type"})
      
    def test_handle_audio_large_file(self):
        large_mock_audio = BytesIO(b"A" * (10 * 1024 * 1024))
        large_mock_audio.name = 'large_audio.wav'

        data = {'audio': (large_mock_audio, 'large_audio.wav')}
        response = self.client.post('/audios', content_type='multipart/form-data', data=data)

        large_mock_audio.close()
        
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json, {"error": "File size exceeds limit"})

    @patch('views.transcribe_audio')
    def test_handle_audio_transcription_failure(self, mock_transcribe):
        mock_transcribe.return_value = None
        
        mock_audio = BytesIO(b"audio data")
        mock_audio.name = 'test_audio.wav'
        data = {'audio': (mock_audio, 'test_audio.wav')}

        response = self.client.post('/audios', content_type='multipart/form-data', data=data)
        
        mock_audio.close()
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Transcription failed"})
        mock_transcribe.assert_called_once()
    
    
    def test_handle_audio_file_not_found(self):
        response = self.client.post('/audios', content_type='multipart/form-data', data={})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "File not found"})
    
    @patch.dict('views.extracted_data_storage', {'12345': {"extracted_data": {"person": ["Jane Smith"]}, "timestamp": time.time()}})
    def test_get_extracted_data(self):
        response = self.client.get('/extracted_data/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"person": ["Jane Smith"]})
    
    def test_get_extracted_data_not_found(self):
        response = self.client.get('/extracted_data/nonexistent_key')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Data not found"})

    def test_cleanup_extracted_data(self):
        extracted_data_storage["old_key"] = {"extracted_data": "old data", "timestamp": time.time() - 7200}
        extracted_data_storage["new_key"] = {"extracted_data": "new data", "timestamp": time.time()}

        cleanup_extracted_data()

        self.assertNotIn("old_key", extracted_data_storage)
        self.assertIn("new_key", extracted_data_storage)
