// Make getDirections accessible globally for inline onclick calls
function getDirections(destination) {
    navigator.geolocation.getCurrentPosition(
      position => {
        let userLocation = `${position.coords.latitude},${position.coords.longitude}`;
        let mapsUrl = `https://www.google.com/maps/dir/${userLocation}/${encodeURIComponent(destination)}`;
        window.open(mapsUrl, "_blank");
      },
      error => {
        console.error("Error getting location:", error);
        alert("Could not get location. Please enable location services.");
      }
    );
  }
  window.getDirections = getDirections; // Expose to global scope
  
  document.addEventListener("DOMContentLoaded", function () {
    // --- Background Image Rotation (only when no results are found) ---
    let backgroundInterval = null;
    const images = [
        "url('/static/img/aloha.jpeg')",
        "url('/static/img/open.jpeg')"
      ];
      
    let currentBgIndex = 0; // Sequential rotation
  
    function changeBackgroundImage() {
      console.log("Rotating background. Current index:", currentBgIndex);
      document.body.style.backgroundImage = images[currentBgIndex];
      document.body.style.backgroundSize = "cover";
      document.body.style.backgroundPosition = "center";
      currentBgIndex = (currentBgIndex + 1) % images.length;
    }
  
    function startBackgroundRotation() {
      console.log("Starting background rotation");
      changeBackgroundImage(); // Set the initial image immediately
      backgroundInterval = setInterval(changeBackgroundImage, 2000);
    }
  
    function stopBackgroundRotation() {
      if (backgroundInterval) {
        console.log("Stopping background rotation");
        clearInterval(backgroundInterval);
        backgroundInterval = null;
      }
    }
  
    // --- Search Form Handling ---
    const searchForm = document.getElementById("searchForm");
    if (searchForm) {
      searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
    
        let query = document.getElementById("searchQuery").value.trim();
        if (!query) {
          console.warn("Empty query provided.");
          return;
        }

        fetch(`/search_places?query=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(data => {
            console.log("API Response:", data.results);
    
            let resultsDiv = document.getElementById("results");
            if (!resultsDiv) {
              console.error("Error: #results div not found in DOM");
              return;
            }
    
            resultsDiv.innerHTML = ""; // Clear previous results
    
            if (data.results && data.results.length > 0) {
              // There are results so stop the background rotation
              stopBackgroundRotation();
              // Explicitly clear the background image by setting it to 'none'
              document.body.style.backgroundImage = "none";
    
              data.results.forEach(place => {
                let photoUrl = place.photos?.[0]?.photo_reference
                  ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${encodeURIComponent(place.photos[0].photo_reference)}&key=AIzaSyDpX3RFvV4L45n5RpKYnqs--0E5GsXJfqw`
                  : "/static/img/default-placeholder.png";
    
                resultsDiv.innerHTML += `
                  <div class="place-container">
                    <h2>${place.name}</h2>
                    <img src="${photoUrl}" alt="${place.name}">
                    <p>📍 Address: ${place.formatted_address}</p>
                    <p>⭐ Rating: ${place.rating ?? "N/A"}/5</p>
                    <p>🕒 Open Now: ${place.opening_hours?.open_now ? "Yes" : "No"}</p>
                    <a href="https://www.google.com/maps/search/?q=${encodeURIComponent(place.name)}" target="_blank">View on Google Maps</a>
                    <button onclick="getDirections('${place.formatted_address}')">Get Directions</button>
                  </div>`;
              });
            } else {
              // No search results: show message and start background rotation.
              resultsDiv.innerHTML = "<p>No results found.</p>";
              if (!backgroundInterval) {
                startBackgroundRotation();
              }
            }
          })
          .catch(error => console.error("Error fetching places:", error));
      });
    } else {
      console.error("Error: #searchForm not found in DOM");
    }
    
    // --- "Back to Top" Functionality ---
    window.addEventListener("scroll", function () {
      const backToTop = document.getElementById("backToTop");
      if (backToTop) {
        backToTop.style.display = window.pageYOffset > 100 ? "block" : "none";
      }
    });
    
    const backToTopButton = document.getElementById("backToTop");
    if (backToTopButton) {
      backToTopButton.addEventListener("click", function (e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
    
    // --- Refresh Button Handling ---
    const refreshButton = document.getElementById("refreshSearchBtn");
    if (refreshButton) {
      refreshButton.addEventListener("click", function () {
        // Clear the search input and results
        document.getElementById("searchQuery").value = "";
        document.getElementById("results").innerHTML = "";
        // Restart background rotation when the search is refreshed.
        if (!backgroundInterval) {
          startBackgroundRotation();
        }
        console.log("Search refreshed.");
      });
    }
  });


  document.body.style.transition = "background 0.5s ease"; // Faster fade effect

  setInterval(() => {
      let colors = ['#e2eafc', "#cae5ff", "#cef4ff", "#dceef3", "ccdbfd","#d9f0ff","#d7e3fc","#f5efff"];
      document.body.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  }, 3000); // Changes color every 2 seconds


  const backgroundEl = document.getElementById('background');

  setInterval(() => {
    const images = [
      "url('/static/img/aloha.jpeg')",
      "url('/static/img/igloo.jpeg')",
      "url('/static/img/surf_shop.jpeg')",
      "url('/static/img/open.jpeg')",
      "url('/static/img/surf_shop.jpeg')",
      "url('/static/img/beach_rest.jpeg')"
    ];
    
    // Fade out the background element
    backgroundEl.style.opacity = 0;
    
    // After the fade-out duration, change image and fade back in
    setTimeout(() => {
      backgroundEl.style.backgroundImage = images[Math.floor(Math.random() * images.length)];
      backgroundEl.style.opacity = 1;
    }, 1000);
    
  }, 5000); // Change the image every 5 seconds
  
  
  