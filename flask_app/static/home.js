  // ----- Video Rotation Code -----
  const videos = [
    '/static/video/surfing.mp4',
    '/static/video/surfing2.mp4',
    '/static/video/surfing3.mp4',
    '/static/video/surfing4.mp4',
    '/static/video/surfing9.mp4',
    '/static/video/surfing6.mp4'

  ];
  let videoIndex = 0;  // Renamed from currentIndex to videoIndex
  const videoEl = document.getElementById('rotatingVideo');

  videoEl.addEventListener('ended', () => {
    // Fade out the video
    videoEl.style.opacity = 0;
    setTimeout(() => {
      videoIndex = (videoIndex + 1) % videos.length;
      videoEl.src = videos[videoIndex];
      videoEl.load();
      videoEl.play().then(() => {
        // Fade the video back in
        videoEl.style.opacity = 1;
      }).catch(error => {
        console.error('Error playing video:', error);
      });
    }, 1000);  // Matches CSS transition duration
  });

  // ----- Quotes Rotation Code -----
  const quotes = [
    "Sometimes, you just have to go with the waves",
    "Let the other guys go; catch another one.",
    "There is no new wave, only the sea",
    "Even the upper end of the river believes in the ocean",
    "Good vibes only: share the wave, share the stoke."
  ];
  let quoteIndex = 0;  // Use a different variable for quotes
  const quoteElement = document.getElementById('quoteText');

  function changeQuote() {
    // Fade out the current quote
    quoteElement.classList.add('fade-out');
    setTimeout(() => {
      // Update the quote index and text
      quoteIndex = (quoteIndex + 1) % quotes.length;
      quoteElement.textContent = quotes[quoteIndex];
      
      // Remove the fade-out class so the new quote fades in
      quoteElement.classList.remove('fade-out');
    }, 1000);  // Wait for the fade-out effect (1 second)
  }
  
  // Rotate the quotes every  9 seconds
  setInterval(changeQuote, 12000);