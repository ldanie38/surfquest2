    // Define your array of video sources (ensure you have at least two different video files)
    const videos = [
        '/static/video/surfing.mp4',
        '/static/video/surfing2.mp4',
        '/static/video/surfing3.mp4',
        '/static/video/surfing5.mp4',
        '/static/video/surfing6.mp4',
        '/static/video/surfing7.mp4',
        '/static/video/surfing9.mp4',
        
        // You can add more video URLs here if desired.
      ];
      
      let currentIndex = 0;
      const videoEl = document.getElementById('rotatingVideo');
  
      // Add an event listener for when the video ends
      videoEl.addEventListener('ended', () => {
        console.log('Video ended, preparing to switch...');
        
        // Fade out the video element by setting opacity to 0
        videoEl.style.opacity = 0;
        
        // Wait for the fade out transition to finish (1 second as defined in CSS)
        setTimeout(() => {
          // Update the video index (cycling back to 0 if at the end)
          currentIndex = (currentIndex + 1) % videos.length;
          console.log('Switching to video:', videos[currentIndex]);
          
          // Change the video source to the next one
          videoEl.src = videos[currentIndex];
          // Reload and play the new video
          videoEl.load();
          videoEl.play()
            .then(() => {
              // Fade the video back in
              videoEl.style.opacity = 1;
            })
            .catch(error => {
              console.error('Error playing video:', error);
            });
        }, 1000); // 1000ms matches the CSS transition duration
      });
