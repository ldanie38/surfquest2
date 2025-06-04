document.getElementById("searchForm").addEventListener("submit", function (event) {
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
                data.results.forEach(place => {
                    let photoUrl = place.photos?.[0]?.photo_reference
                        ? `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${encodeURIComponent(place.photos[0].photo_reference)}&key=AIzaSyDpX3RFvV4L45n5RpKYnqs--0E5GsXJfqw`
                        : "/static/img/default-placeholder.png";

                    resultsDiv.innerHTML += `
                        <div class="place-container">
                            <h2>${place.name}</h2>
                            <img src="${photoUrl}" alt="${place.name}">
                            <p>📍 Address: ${place.formatted_address}</p>
                            <p>⭐ Rating: ${place.rating ?? 'N/A'}/5</p>
                            <p>🕒 Open Now: ${place.opening_hours?.open_now ? "Yes" : "No"}</p>
                            <a href="https://www.google.com/maps/search/?q=${encodeURIComponent(place.name)}" target="_blank">View on Google Maps</a>
                            <button onclick="getDirections('${place.formatted_address}')">Get Directions</button>
                        </div>`;
                });
            } else {
                resultsDiv.innerHTML = "<p>No results found.</p>";
            }
        })
        .catch(error => console.error("Error fetching places:", error));
});

function getDirections(destination) {
    navigator.geolocation.getCurrentPosition(
        position => {
            let userLocation = `${position.coords.latitude},${position.coords.longitude}`;
            let mapsUrl = `https://www.google.com/maps/dir/${userLocation}/${encodeURIComponent(destination)}`;
            window.open(mapsUrl, '_blank');
        },
        error => {
            console.error("Error getting location:", error);
            alert("Could not get location. Please enable location services.");
        }
    );
}

window.addEventListener('scroll', function () {
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        backToTop.style.display = window.pageYOffset > 100 ? 'block' : 'none';
    }
});

const backToTopButton = document.getElementById("backToTop");
if (backToTopButton) {
    backToTopButton.addEventListener("click", function (e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
