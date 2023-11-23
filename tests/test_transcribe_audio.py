import unittest
from unittest.mock import patch, mock_open
from transcribe_audio import transcribe_audio

class TestTranscribeAudio(unittest.TestCase):
    
    @patch('transcribe_audio.open', new_callable=mock_open, read_data="fake audio data")
    @patch('transcribe_audio.OpenAI')
    def test_transcribe_audio_sucess(self, mock_openai, mock_file):
        mock_openai.return_value.audio.transcriptions.create.return_value = {"text": "Sample transcription"}
        
        result = transcribe_audio("path/to/fake/audio/file")
        
        self.assertEqual(result, "Sample transcription")
        self.assertIsInstance(result, str)
        mock_file.assert_called_once_with("path/to/fake/audio/file", 'rb')
        mock_openai.return_value.audio.transcriptions.create.assert_called_once()
        
    
    @patch('transcribe_audio.open', new_callable=mock_open, read_data="fake audio data")
    @patch('transcribe_audio.OpenAI')
    def test_transcribe_audio_failure(self, mock_openai, mock_file):
        mock_openai.return_value.audio.transcriptions.create.return_value = {}
        
        result = transcribe_audio("path/to/fake/audio/file")
        
        self.assertIsNone(result)
        mock_file.assert_called_once_with("path/to/fake/audio/file", 'rb')
        mock_openai.assert_called_once()
        mock_openai.return_value.audio.transcriptions.create.assert_called_once()
