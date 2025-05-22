document.addEventListener("DOMContentLoaded", function() {
    // ===================
    // Like Button Handler
    // ===================
    document.querySelectorAll(".like-button").forEach(button => {
      button.addEventListener("click", async function() {
        const postId = this.dataset.postId;
        try {
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
        } catch (error) {
          console.error("Error liking post:", error);
        }
      });
    });
  
    // =====================
    // Comment Button Toggle
    // =====================
    document.querySelectorAll(".comment-button").forEach(button => {
      button.addEventListener("click", function() {
        const postId = this.dataset.postId;
        const commentSection = document.getElementById(`comments-container-${postId}`);
        const commentForm = document.getElementById(`comment-form-${postId}`);
  
        // Toggle comments container display
        if (commentSection) {
          commentSection.style.display =
            commentSection.style.display === "none" ? "block" : "none";
        }
  
        // Toggle form display
        if (commentForm) {
          commentForm.style.display =
            commentForm.style.display === "none" ? "block" : "none";
        } else {
          console.error(`Comment form not found for post ID: ${postId}`);
        }
      });
    });
  
    // ======================================
    // Comment Submission (Main Comment Form)
    // ======================================
    document.querySelectorAll("form.comment-form").forEach(form => {
      form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent page reload
  
        // Prevent duplicate submissions
        if (this.dataset.submitting === "true") return;
        this.dataset.submitting = "true";
  
        const postId = this.querySelector("input[name='post_id']").value;
        const content = this.querySelector("textarea").value.trim();
  
        if (!content) {
          alert("Comment cannot be empty.");
          this.dataset.submitting = "false";
          return;
        }
  
        try {
          const response = await fetch(`/blog/${postId}/comment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content })
          });
  
          if (response.ok) {
            const data = await response.json();
            // Create and append the new comment element
            const newComment = document.createElement("div");
            newComment.classList.add("comment");
            newComment.innerHTML = `<strong>${data.username}:</strong> ${data.content}`;
            const commentsContainer = document.getElementById(`comments-container-${postId}`);
            if (commentsContainer) {
              commentsContainer.appendChild(newComment);
            } else {
              console.error(`Comments container not found for post ID: ${postId}`);
            }
            // Clear the textarea after submission
            this.querySelector("textarea").value = "";
          } else {
            alert("Failed to post comment.");
            console.error("Error submitting comment:", response);
          }
        } catch (error) {
          console.error("AJAX request failed:", error);
        }
        // Reset submission flag
        setTimeout(() => {
          this.dataset.submitting = "false";
        }, 500);
      });
    });
  
    // ============================
    // Reply Button Toggle Handler
    // ============================
    document.querySelectorAll(".reply-button").forEach(btn => {
      btn.addEventListener("click", function() {
        const commentId = this.dataset.commentId;
        const form = document.getElementById(`reply-form-${commentId}`);
        if (form) {
          form.style.display = form.style.display === "none" ? "block" : "none";
        }
      });
    });
  
    // ========================================
    // Reply Submission (Nested Reply Form)
    // ========================================
    document.querySelectorAll("form.reply-form").forEach(form => {
      form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent page reload
  
        const commentId = this.dataset.parentCommentId;
        const postId = this.querySelector("input[name='post_id']").value;
        const content = this.querySelector("textarea").value.trim();
  
        if (!content) {
          alert("Reply cannot be empty.");
          return;
        }
  
        try {
          const response = await fetch(`/blog/${postId}/comment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content, parent_comment_id: commentId })
          });
  
          if (response.ok) {
            const data = await response.json();
            // Create and append the new reply element
            const newReply = document.createElement("div");
            newReply.classList.add("nested-comment");
            newReply.innerHTML = `<strong>${data.username}:</strong> ${data.content}`;
  
            const repliesContainer = document.getElementById(`replies-container-${commentId}`);
            if (repliesContainer) {
              repliesContainer.appendChild(newReply);
            } else {
              console.error(`Replies container not found for comment ID: ${commentId}`);
            }
            // Clear the textarea after submission
            this.querySelector("textarea").value = "";
          } else {
            alert("Failed to post reply.");
            console.error("Error submitting reply:", response);
          }
        } catch (error) {
          console.error("AJAX request failed:", error);
        }
      });
    });
  
    // ==================
    // Image Rotation
    // ==================
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
      "static/img/day.jpg"
    ];
  
    let imageIndex = 0;
    function changeImage() {
      const imgElement = document.getElementById("surfImage");
      if (imgElement) {
        // Fade out the current image
        imgElement.style.opacity = 0;
        
        setTimeout(() => {
          imageIndex = (imageIndex + 1) % images.length;
          imgElement.src = images[imageIndex];
          // Fade back in once the new image has loaded
          imgElement.onload = () => {
            imgElement.style.opacity = 1;
          };
        }, 2000);
      }
    }
    setInterval(changeImage, 8000);
  
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
  });
  