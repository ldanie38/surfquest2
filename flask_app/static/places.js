
// Global function for inline onclick calls (e.g. "Get Directions")
function getDirections(destination) {
  navigator.geolocation.getCurrentPosition(
    position => {
      const userLocation = `${position.coords.latitude},${position.coords.longitude}`;
      const mapsUrl = `https://www.google.com/maps/dir/${userLocation}/${encodeURIComponent(destination)}`;
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
  //////////////////////////////////////////////////
  // Background Color Rotation (Always Active)
  //////////////////////////////////////////////////
  document.body.style.transition = "background 0.5s ease";
  setInterval(() => {
    const colors = ['#e2eafc', '#cae5ff', '#cef4ff', '#dceef3', '#ccdbfd', '#d9f0ff', '#d7e3fc', '#f5efff'];
    document.body.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  }, 3000);

  //////////////////////////////////////////////////
  // Background Image Rotation (Sequential Order)
  // Only runs when the #results element is empty
  //////////////////////////////////////////////////
  const backgroundEl = document.getElementById("background");
  const bgImages = [
    "url('/static/img/aloha.jpeg')",
    "url('/static/img/open.jpeg')",
    "url('/static/img/igloo.jpeg')",
    "url('/static/img/surf_shop.jpeg')",
    "url('/static/img/beach_rest.jpeg')",
    "url('/static/img/gym.jpeg')",
    "url('/static/img/waw.jpeg')",
    "url('/static/img/tacos.jpeg')",
    "url('/static/img/disco.jpeg')",
    "url('/static/img/room.jpeg')"
  ];
  let currentBgIndex = 0;
  let backgroundInterval = null;

  function changeBackgroundImage() {
    if (backgroundEl) {
      backgroundEl.style.backgroundImage = bgImages[currentBgIndex];
      backgroundEl.style.backgroundSize = "cover";
      backgroundEl.style.backgroundPosition = "center";
      // Move sequentially – once reached the end, wrap to the beginning.
      currentBgIndex = (currentBgIndex + 1) % bgImages.length;
    }
  }

  function startBackgroundRotation() {
    console.log("Starting background image rotation");
    // Set the initial image immediately.
    changeBackgroundImage();
    backgroundInterval = setInterval(changeBackgroundImage, 4000);
  }

  function stopBackgroundRotation() {
    if (backgroundInterval) {
      console.log("Stopping background image rotation");
      clearInterval(backgroundInterval);
      backgroundInterval = null;
    }
  }

  // On load, if there are no search results, start rotating the background images.
  const resultsDiv = document.getElementById("results");
  if (resultsDiv && resultsDiv.childElementCount === 0) {
    startBackgroundRotation();
  }

  //////////////////////////////////////////////////
  // Search Form Handling
  //////////////////////////////////////////////////
  const searchForm = document.getElementById("searchForm");
  if (searchForm) {
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const query = document.getElementById("searchQuery").value.trim();
      if (!query) {
        console.warn("Empty query provided.");
        return;
      }

      fetch(`/search_places?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          console.log("API Response:", data.results);
          const resultsDiv = document.getElementById("results");
          if (!resultsDiv) {
            console.error("Error: #results div not found in DOM");
            return;
          }
          // Clear previous results.
          resultsDiv.innerHTML = "";

          if (data.results && data.results.length > 0) {
            // Stop background image rotation when search results are found.
            stopBackgroundRotation();
            if (backgroundEl) {
              backgroundEl.style.backgroundImage = "none";
            }

            data.results.forEach(place => {
              const photoUrl = (place.photos && place.photos[0] && place.photos[0].photo_reference)
                ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${encodeURIComponent(place.photos[0].photo_reference)}&key=AIzaSyDpX3RFvV4L45n5RpKYnqs--0E5GsXJfqw`
                : "/static/img/default-placeholder.png";

              resultsDiv.innerHTML += `
                <div class="place-container">
                  <h2>${place.name}</h2>
                  <img src="${photoUrl}" alt="${place.name}">
                  <p>📍 Address: ${place.formatted_address}</p>
                  <p>⭐ Rating: ${place.rating ?? "N/A"}/5</p>
                  <p>🕒 Open Now: ${place.opening_hours && place.opening_hours.open_now ? "Yes" : "No"}</p>
                  <a href="https://www.google.com/maps/search/?q=${encodeURIComponent(place.name)}" target="_blank">View on Google Maps</a>
                  <button onclick="getDirections('${place.formatted_address}')">Get Directions</button>
                </div>`;
            });
          } else {
            // If no results, display a "No results found" message and ensure the background rotation runs.
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




  
  //////////////////////////////////////////////////
  // Refresh Button Handling
  //////////////////////////////////////////////////
  const refreshButton = document.getElementById("refreshSearchBtn");
  if (refreshButton) {
    refreshButton.addEventListener("click", function () {
      // Clear the search input and results.
      document.getElementById("searchQuery").value = "";
      document.getElementById("results").innerHTML = "";
      // Restart background image rotation on refresh if it's not already active.
      if (!backgroundInterval) {
        startBackgroundRotation();
      }
      console.log("Search refreshed.");
    });
  }
});

  //////////////////////////////////////////////////
  // "Back to Top" Functionality
  //////////////////////////////////////////////////

// Scroll arrows logic
document.addEventListener("DOMContentLoaded", () => {
  console.log("Arrow script loaded");   // sanity check
  const upBtn   = document.getElementById("scroll-up");
  const downBtn = document.getElementById("scroll-down");
  if (!upBtn || !downBtn) {
    console.error("Scroll buttons not found in DOM");
    return;
  }

  // Show/hide the up arrow after you scroll half a screen
  window.addEventListener("scroll", () => {
    upBtn.classList.toggle("d-none", window.scrollY < window.innerHeight / 2);
  });

  // Jump up
  upBtn.addEventListener("click", () => {
    window.scrollBy({ top: -window.innerHeight, behavior: "smooth" });
  });

  // Jump down
  downBtn.addEventListener("click", () => {
    window.scrollBy({ top: window.innerHeight, behavior: "smooth" });
  });
});
