/* LIKE AND UNLIKE FUNCTIONALITY FOR POSTS
Function to update like counts and pluralization for posts */
function updateLikeCounts() {
  document.querySelectorAll('.like-count').forEach(function (likeCount) {
    var count = parseInt(likeCount.textContent);
    var count_str = count === 1 ? 'like' : 'likes';
    likeCount.textContent = count + ' ' + count_str;
  });
}

// Function to update like button UI
function updateLikeButtonUI(postSlug, data) {
  // Update both detail like buttons' UI
  document.querySelectorAll(`[data-post-slug="${postSlug}"]`).forEach(function (likeButton) {
    var like_icon = likeButton.querySelector('.article-like-style');
    var like_count = likeButton.querySelector('.like-count');

    if (data.liked) {
      like_icon.style.color = 'salmon';
      like_count.textContent = data.likes_count + ' ' + data.count_str;
      like_count.style.color = 'salmon';
    } else {
      like_icon.style.color = 'white';
      like_count.textContent = data.likes_count + ' ' + data.count_str;
      like_count.style.color = '';
    }
  });
}

// Update like counts and pluralization on page load
updateLikeCounts();

// Update the count string when the like buttons are clicked
document.querySelectorAll('[data-post-slug]').forEach(function (likeButton) {
  likeButton.addEventListener('click', function (e) {
    e.preventDefault();
    var likeURL = likeButton.getAttribute('data-href');
    var postSlug = likeButton.getAttribute('data-post-slug');

    if (likeURL) {
      fetch(likeURL, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest', // Include this header for Django to detect AJAX requests
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          console.log(data);

          // Update both detail like buttons' UI
          updateLikeButtonUI(postSlug, data);

          // Update like counts on the page
          updateLikeCounts();
        })
        .catch(function (error) {
          console.error(error);
          console.error('error');
        });
    }
  });
});

/* LIKE AND UNLIKE FUNCTIONALITY FOR COMMENTS
Function to update comment like counts and pluralization */
function updateCommentLikeCounts() {
  console.log('Updating comment like counts and pluralization...');
  document.querySelectorAll('.like-count').forEach(function (likeCount) {
    var count = parseInt(likeCount.textContent);
    var count_str = count === 1 ? 'like' : 'likes';
    likeCount.textContent = count + ' ' + count_str;
  });
}

// Function to update comment like button UI
function updateCommentLikeButtonUI(commentId, data) {
  console.log('Updating comment like button UI...');

  // Select the comment like button
  var likeButton = document.querySelector(`[data-comment-id="${commentId}"]`);
  if (!likeButton) {
    console.error('Comment like button not found for comment ID:', commentId);
    return;
  }

  // Update comment like button UI
  var like_icon = likeButton.querySelector('.fas.fa-heart');
  var like_count = likeButton.querySelector('.like-count');

  if (like_icon && like_count) {
    if (data.liked) {
      like_icon.style.color = 'salmon';
      like_count.textContent = data.likes_count + ' ' + data.count_str;
      like_count.style.color = 'salmon';
    } else {
      like_icon.style.color = 'white'; // Change to your desired color
      like_count.textContent = data.likes_count + ' ' + data.count_str;
      like_count.style.color = ''; // Remove color style if not needed
    }
  } else {
    console.error('Comment like button UI elements not found for comment ID:', commentId);
  }
}

// Update comment like counts and pluralization on page load
updateCommentLikeCounts();

// Update the count string when the comment like buttons are clicked
document.querySelectorAll('[data-comment-id]').forEach(function (likeButton) {
  likeButton.addEventListener('click', function (e) {
    e.preventDefault();
    var likeURL = likeButton.getAttribute('data-href');
    var commentId = likeButton.getAttribute('data-comment-id');

    if (likeURL) {
      console.log('Click event triggered for comment like button with comment ID:', commentId);

      fetch(likeURL, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest', // Include this header for Django to detect AJAX requests
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          console.log('Response from comment like API:', data);

          // Update comment like button UI
          updateCommentLikeButtonUI(commentId, data);

          // Update comment like counts on the page
          updateCommentLikeCounts();
        })
        .catch(function (error) {
          console.error('Error:', error);
        });
    }
  });
});


// delete post functionality

/* $(document).ready(function(){
  $('#delete-post-form').submit(function(event){
      event.preventDefault()
      
      var formData = $(this).serialize()
      $.ajax({
          url: $(this).attr('action'),
          type: 'POST',
          data: formData,
          headers: {
              'X-CSRFToken': '{{ csrf_token }}'
          },
          success: function(){
              window.location.href = '/'
          }
      })
  })
})
 */

document.addEventListener("DOMContentLoaded", function () {
  var deleteForm = document.getElementById("delete-post-form");

  if (deleteForm) {
      deleteForm.addEventListener("submit", function (event) {
          event.preventDefault();

          var formData = new FormData(deleteForm);
          var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

          fetch(deleteForm.getAttribute("action"), {
              method: "POST",
              body: formData,
              headers: {
                  "X-CSRFToken": csrfToken,
              },
          })
              .then(function (response) {
                  if (response.ok) {
                      // Redirect to the desired page upon successful delete
                      window.location.href = "/";
                  } else {
                      // Handle the error response here
                      console.error("Error deleting post");
                  }
              })
              .catch(function (error) {
                  console.error("Fetch error: " + error);
              });
      });
  }
});

// Adding comment functionality

document.addEventListener("DOMContentLoaded", function () {
  var batch_size = 10; // Set the batch size here
  var totalComments = 0;
  var displayedComments = 0;

  // Function to load more comments
  function loadMoreComments() {
    var offset = displayedComments;
    var slug = document.getElementById("comment-form").getAttribute("data-slug");
    var loadMoreURL = `/load_more_comments/${slug}/${offset}/`;

    fetch(loadMoreURL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }
        return response.json();
      })
      .then((data) => {
        if (data.length > 0) {
          // Render the new comments on the page
          data.forEach((commentData) => {
            renderComment(commentData);
          });
          // Update the 'offset' attribute of the "Load more comments" button
          displayedComments += data.length;
          // Hide the "Load more comments" button if no more comments to load
          if (displayedComments >= totalComments) {
            document.getElementById("load-more-button").style.display = "none";
          }
        } else {
          // Hide the "Load more comments" button if no more comments to load
          document.getElementById("load-more-button").style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  // Show only the first batch of comments
  displayedComments = batch_size;
  console.log("Total comments:", totalComments);
  console.log("Batch size:", batch_size);

  // Function to render a new comment on the page
  function renderComment(commentData) {
    var commentHtml = `
      <div class="comment">
        <div class="comment-header">
          <h3>${commentData.user}</h3>
          <span class="timestamp">${commentData.date_posted}</span>
        </div>
        <div class="comment-body">
          <p>${commentData.comment}</p>
        </div>
        <div class="comment-footer">
          <button class="like-button"><i class="fas fa-heart"></i>Like</button>
          <button class="like-button"><i class="fa-solid fa-trash"></i>Delete</button>
        </div>
        <hr>
        <div class="child-comments">
          <!-- Child comments go here (if any) -->
        </div>
      </div>`;

    document
      .getElementById("comments-section")
      .insertAdjacentHTML("afterbegin", commentHtml);
  }

  // Function to fetch comments from the server and render them on the page
  function fetchAndRenderComments() {
    var slug = document.getElementById("comment-form").getAttribute("data-slug");
    var commentListURL = `/comments/${slug}/`;

    fetch(commentListURL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Fetched comments:", data);
        // Update the total number of comments
        totalComments = data.length;
        console.log("Total comments:", totalComments);
        // Hide the "Load more comments" button if no more comments to load
        if (totalComments <= displayedComments) {
          document.getElementById("load-more-button").style.display = "none";
        } else {
          document.getElementById("load-more-button").style.display = "block";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  // Fetch and render comments when the page loads
  fetchAndRenderComments();

  // Fetch and render more comments when the "Load more comments" button is clicked
  document.getElementById("load-more-button").addEventListener("click", function () {
    loadMoreComments();
  });

  // Function to submit the comment form using Fetch API
  document
    .getElementById("comment-form")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      var commentText = document.getElementById("comment-textarea").value.trim();
      if (commentText !== "") {
        var formData = new FormData(this);
        var slug = this.getAttribute("data-slug");
        var commentSubmitURL = `/comment_submit/${slug}/`;

        fetch(commentSubmitURL, {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok.");
            }
            return response.json();
          })
          .then((data) => {
            // Clear the comment textarea after successful submission
            document.getElementById("comment-textarea").value = "";
            // Render the new comment on the page
            renderComment(data);
            displayedComments += 1;
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    });

  // Function to get CSRF token from cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
