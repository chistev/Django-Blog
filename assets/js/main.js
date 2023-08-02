// Like and unlike functionality

// Generate the initial count string on page load
$('.like-count').each(function() {
  var count = parseInt($(this).text());
  var count_str = count === 1 ? '1 like' : count + ' likes';
  $(this).text(count_str);
});

// Update the count string when the like buttons are clicked
$('.like-button').click(function(e) {
  e.preventDefault();
  var this_ = $(this);
  var likeURL = this_.attr('data-href');
  var postSlug = this_.attr('data-post-slug'); // Get the post ID

  if (likeURL) {
    $.ajax({
      url: likeURL,
      method: 'GET',
      data: {},
      success: function(data) {
        console.log(data);
        var count = data.likes_count;
        var count_str = data.count_str;

        // Update the like count and style for the clicked button
        var clickedButton = $('.like-button[data-post-slug="' + postSlug + '"]');
        var like_icon = clickedButton.find('.article-like-style');
        var like_count = clickedButton.find('.like-count');

        if (data.liked) {
          like_icon.css('color', 'salmon');
          like_count.text(count + ' ' + count_str);
          like_count.css('color', 'salmon');
        } else {
          like_icon.css('color', 'white');
          like_count.text(count + ' ' + count_str);
          like_count.css('color', '');
        }
      },
      error: function(error) {
        console.error(error);
        console.error('error');
      }
    });
  }
});


// delete post functionality

$(document).ready(function(){
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
          <button class="comment-button"><i class="fa-solid fa-comment"></i>Reply</button>
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
