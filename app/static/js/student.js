window.onload = function () {
    const comment_node = document.getElementById("comments")
    comment_node.textContent = comment_node.getAttribute("data-comment")

}

function removeStudent(id) {
    // Submit the form
    console.log("Student ID: " + id);

    $("#removeStudentModal").modal('hide');

    window.location.href = '/remove_from_session?student_id=' + id

    // redirect to remove student with student information

    return false; // Ensure no unexpected behaviour
}

function detectChanges(commentSuggestions) {
    let inputString = $('#comments').val();
    console.log(inputString);
    commentSuggestions.forEach(suggestion => {
        if (inputString.includes(suggestion.text())) {
            suggestion.fadeOut("fast", "linear")
        }
        else {
            suggestion.fadeIn("fast", "linear")
        }
    });
}

$(document).ready(function () {
    const commentSuggestions = [];
$('.suggestion').each(function () {
    commentSuggestions.push($(this));
});

    detectChanges(commentSuggestions);
    $('#comments').on("change keyup paste", function () {
        detectChanges(commentSuggestions);
    })

    $('.suggestion').on('click', function () {
        var suggestedText = $(this).text();
        var commentsField = $('#comments');
        $(this).fadeOut("fast", "linear")

        commentsField.val(function (i, text) {
            return text + (text ? ', ' : '') + suggestedText;
        });
    });
});