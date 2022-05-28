$('.button-like-dislike').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid');
    $.ajax('/vote/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid
        }
    }).done(function(data) {
        $("#" + qid).html("").append(data['rating']);
        if (action === 'like') {
            $("#like" + qid).prop('hidden', true);
            $("#dislike" + qid).prop('hidden', false);
        } else {
            $("#dislike" + qid).prop('hidden', true);
            $("#like" + qid).prop('hidden', false);
        }
    });
});


$('.button-like-dislike_answer').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        aid = $this.data('aid');
    $.ajax('/vote_answer/', {
        method: 'POST',
        data: {
            action: action,
            aid: aid
        }
    }).done(function(data) {
        $("#answer" + aid).html("").append(data['rating']);
        if (action === 'like') {
            $("#answer_like" + aid).prop('hidden', true);
            $("#answer_dislike" + aid).prop('hidden', false);
        } else {
            $("#answer_dislike" + aid).prop('hidden', true);
            $("#answer_like" + aid).prop('hidden', false);
        }
    });
});


$('.js-current').click(function(ev) {
    ev.preventDefault();
    var $this = $(this),
        aid = $this.data('aid'),
        qid = $this.data('qid');
    $.ajax('/vote_current/', {
        method: 'POST',
        data: {
            aid: aid,
            qid: qid
        }
    }).done(function(data) {
        $("#correct" + aid).prop('checked', data['correct']);
        $("#correct" + data['incorrect']).prop('checked', false);
        console.log("RESPONSE: ", data)
    });
});
