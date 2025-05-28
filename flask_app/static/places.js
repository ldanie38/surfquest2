document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let query = document.getElementById("searchQuery").value;

    fetch(`/search_places?query=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data.results); // Debugging output

            let resultsDiv = document.getElementById("results");

            if (!resultsDiv) {
                console.error("Error: #results div not found in HTML");
                return;
            }

            resultsDiv.innerHTML = ""; // Clear previous results

            if (data.results && data.results.length > 0) {
                data.results.forEach(place => {
                    // 🔥 Move `photoUrl` inside the loop!
                    let photoUrl = place.photos && place.photos.length > 0 
                        ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${encodeURIComponent(place.photos[0].photo_reference)}&key=AIzaSyDpX3RFvV4L45n5RpKYnqs--0E5GsXJfqw`
                        : "/static/img/default-placeholder.png";

                    // 🔥 Log the generated photo URL in console
                    console.log("Photo URL:", photoUrl);
                    resultsDiv.innerHTML += `
                        <div class="place-container">
                            <h2>${place.name}</h2>
                            <img src="${photoUrl}" alt="${place.name}">
                            <p>📍 Address: ${place.formatted_address}</p>
                            <p>⭐ Rating: ${place.rating ? place.rating : 'N/A'}/5</p>
                            <p>🕒 Open Now: ${place.opening_hours ? (place.opening_hours.open_now ? "Yes" : "No") : "Unknown"}</p>
                            <a href="https://www.google.com/maps/search/?q=${encodeURIComponent(place.name)}" target="_blank">View on Google Maps</a>
                        </div>`;

                    console.log("Photo Reference:", place.photos ? place.photos[0].photo_reference : "No photo available");
                });
            } else {
                resultsDiv.innerHTML = "<p>No results found.</p>";
            }
        })
        .catch(error => console.error("Error fetching places:", error));
});


// Function to get directions using user's actual location
function getDirections(destination) {
    navigator.geolocation.getCurrentPosition(
        position => {
            let userLocation = `${position.coords.latitude},${position.coords.longitude}`;
            let mapsUrl = `https://www.google.com/maps/dir/${userLocation}/${encodeURIComponent(destination)}`;
            window.open(mapsUrl, '_blank'); // Open Google Maps with real user location
        },
        error => {
            console.error("Error getting location:", error);
            alert("Could not get location. Please enable location services.");
        }
    );
}

  
    // ============================
    // "Back to Top" Button Handler
    // ============================
    window.addEventListener('scroll', function() {
        const backToTop = document.getElementById('backToTop');
        if (window.pageYOffset > 100) {
          backToTop.style.display = 'block';
        } else {
          backToTop.style.display = 'none';
        }
      });
    
      const backToTopButton = document.getElementById("backToTop");
      if (backToTopButton) {
        backToTopButton.addEventListener("click", function(e) {
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      }
