// Like and unlike functionality

// Generate the initial count string on page load
$('.like-count').each(function() {
    var count = parseInt($(this).text());
    var count_str = count === 1 ? '1 like' : count + ' likes';
    $(this).text(count_str);
  });

  // Update the count string when the like button is clicked
$('.like-button').click(function(e){
    e.preventDefault()
    var this_ = $(this)
    var likeURL = this_.attr('data-href')

     if (likeURL){
        $.ajax({
            url: likeURL,
            method: 'GET',
            data: {},
            success: function(data){
                console.log(data)
                var count = data.likes_count
                var count_str = data.count_str
                var like_icon = this_.find('.fas')
                var like_count = this_.find('.like-count')
                
                if (data.liked){
                    like_icon.css('color', 'salmon')
                    like_count.text(count + ' ' + count_str)
                    like_count.css('color', 'salmon')
                }
                else{
                    like_icon.css('color', 'white')
                    like_count.text(count + ' ' + count_str)
                    like_count.css('color', '')
                }
            }, error: function(error){
                console.error(error);
                console.error('error')
            }
        })
    }
})

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