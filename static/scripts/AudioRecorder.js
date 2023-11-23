let mediaRecorder;
let audioChunks = [];
navigator.mediaDevices.getUserMedia({ audio: true })
  .then((stream) => {
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });

      // Send the recorded audio to the Flask route
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recorded_audio.mp3');

      fetch('http://localhost:5000/audios', {
        method: 'POST',
        body: formData,
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text(); // You can handle the response from the Flask route here
      })
      .then(responseText => {
        console.log(responseText);
      })
      .catch(error => {
        console.error('Error sending audio to Flask route:', error);
      });

      // You can also reset the audioChunks array for the next recording
      audioChunks = [];
    };

    document.getElementById('startRecord').addEventListener('click', () => {
      mediaRecorder.start();
      document.getElementById('startRecord').disabled = true;
      document.getElementById('stopRecord').disabled = false;
    });

    document.getElementById('stopRecord').addEventListener('click', () => {
      mediaRecorder.stop();
      document.getElementById('startRecord').disabled = false;
      document.getElementById('stopRecord').disabled = true;
    });
  })
  .catch((error) => {
    console.error('Error accessing microphone:', error);
  });
