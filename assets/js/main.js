// Like and unlike functionality

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
                    var like_icon = this_.find('.fas')
                    var like_count = this_.find('.like-count')
                if (data.liked){
                    like_icon.css('color', 'salmon')
                    like_count.text(count + ' likes')
                    like_count.css('color', 'salmon')
                }
                else{
                    like_icon.css('color', 'white')
                    like_count.text(count + ' likes')
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

/* $(document).ready(function(){
    $('.delete-button').click(function(){
        console.log("it works")
        if(confirm('Are you sure you want to delete this post?')) {
            var post_slug = '{{ post.slug }}'
            $.ajax({
                url: '/article/' + post_slug + '/delete/',
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                success: function(){
                    window.location.href = '/'
                }
            })
        }
})
}) */

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