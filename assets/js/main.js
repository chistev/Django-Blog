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