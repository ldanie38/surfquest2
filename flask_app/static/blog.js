

    // Like Button Handler
    document.querySelectorAll(".like-button").forEach(button => {
        button.addEventListener("click", async function() {
            const postId = this.dataset.postId;
            const response = await fetch("/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ post_id: postId })
            });

            const data = await response.json();
            if (data.success) {
                this.querySelector(".like-count").textContent = data.likes;
                this.disabled = true;
            } else {
                console.log(data.message);
            }
        });
    });


document.addEventListener("DOMContentLoaded", function() {
    // Like Button Handler
    document.querySelectorAll(".like-button").forEach(button => {
        button.addEventListener("click", async function() {
            const postId = this.dataset.postId;
            const response = await fetch("/like", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ post_id: postId })
            });

            const data = await response.json();
            if (data.success) {
                this.querySelector(".like-count").textContent = data.likes;
                this.disabled = true;
            } else {
                console.log(data.message);
            }
        });
    });

    // Comment Button Toggle (Ensures both comments & form show)
    document.querySelectorAll(".comment-button").forEach(button => {
        button.addEventListener("click", function() {
            const postId = this.dataset.postId;
            console.log(`Clicked Comment Button for Post ID: ${postId}`);
            const commentSection = document.getElementById(`comments-container-${postId}`);
            const commentForm = document.getElementById(`comment-form-${postId}`);

            // Toggle comments container display
            if (commentSection) {
                commentSection.style.display = commentSection.style.display === "none" ? "block" : "none";
            }

            // Toggle form display
            if (commentForm) {
                commentForm.style.display = commentForm.style.display === "none" ? "block" : "none";
            } else {
                console.error(`Comment form not found for post ID: ${postId}`);
            }
        });
    });

    // Comment Submission via AJAX: Only select form elements
    document.querySelectorAll("form.comment-form").forEach(form => {
        form.addEventListener("submit", async function(event) {
            event.preventDefault(); // Prevent default page reload

            // If already submitting, prevent duplicate execution
            if (this.dataset.submitting === "true") {
                return;
            }
            this.dataset.submitting = "true";

            const postId = this.querySelector("input[name='post_id']").value;
            const content = this.querySelector("textarea").value.trim();

            console.log(`Submitting comment for post ID: ${postId}, content: ${content}`);

            if (!content) {
                alert("Comment cannot be empty.");
                this.dataset.submitting = "false"; // Reset for retry
                return;
            }

            // Send AJAX request to submit the comment
            try {
                const response = await fetch(`/blog/${postId}/comment`, {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: new URLSearchParams({ content })
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log("Comment submitted successfully!", data);
                    
                    // Append new comment dynamically
                    const newComment = document.createElement("p");
                    newComment.innerHTML = `<strong>${data.username}:</strong> ${data.content}`;
                    document.getElementById(`comments-container-${postId}`).appendChild(newComment);
                    
                    // Clear textarea after submission
                    this.querySelector("textarea").value = "";
                } else {
                    alert("Failed to post comment.");
                    console.error("Error submitting comment:", response);
                }
            } catch (error) {
                console.error("AJAX request failed:", error);
            }

            // Reset submission flag after a short delay
            setTimeout(() => {
                this.dataset.submitting = "false";
            }, 500);
        }, { once: true }); // Ensures event fires only once per form
    });
});

/* img rotation*/
document.addEventListener("DOMContentLoaded", function() {
    const images = [
        "static/img/bad_ass.jpg",
        "static/img/drone_road_waves.jpg",
        "static/img/surfer_on_wave.jpg",
        "static/img/index.jpg",
        "static/img/dreamy_surfing.jpg",
        "static/img/trees.jpg",
        "static/img/looks_like_whitches.jpg",
        "static/img/chica.jpg",
        "static/img/so_pretty.jpg",
        "static/img/suffing.jpg",
        "static/img/whitches_rock.jpg",
        "static/img/tarzan.jpg",
        "static/img/boat_surf.jpg",
        "static/img/crock.jpg",
        "static/img/yahoo.jpg",
        "static/img/day.jpg",

    ];
  
    let index = 0;
    
    function changeImage() {
        const imgElement = document.getElementById("surfImage");
        if (imgElement) {
            // Fade out
            imgElement.style.opacity = 0;
            
            // After the fade out, change the image and fade back in
            setTimeout(() => {
                index = (index + 1) % images.length;
                imgElement.src = images[index];
                
                // When the new image has loaded, fade in
                imgElement.onload = () => {
                    imgElement.style.opacity = 1;
                };
            }, 2000); // Wait 1 second which matches the CSS transition duration
        }
    }
  
    setInterval(changeImage, 8000); // Change every 5 seconds
  });

    // Show or hide the "Back to Top" button based on scroll position
    window.addEventListener('scroll', function() {
        const backToTop = document.getElementById('backToTop');
        if (window.pageYOffset > 100) { // Change this value if needed
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    });
  
    // Scroll smoothly to the top when the button is clicked
    document.getElementById("backToTop").addEventListener("click", function(e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

