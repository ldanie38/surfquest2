

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

