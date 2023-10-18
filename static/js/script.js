$(document).ready(function () {
    var $text = $('#mainContent');
    $text.hide();

    function loadAndShowContent(href, newTitle) {
        $text.fadeOut(1000, function() {
            $text.load(href + ' #mainContent > *', function() {
                $text.fadeIn(1000);
                updateTitle(newTitle);
            });
        });
    }

    function updateTitle(newTitle) {
        $('title').text(newTitle);
    }

    $('.toggleButton').click(function (event) {
        var href = $(this).attr('href');
        var newTitle = $(this).data('title');
        loadAndShowContent(href, newTitle);
        event.preventDefault();
    });
});

document.getElementById('skillForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var idValue = document.querySelector('.inputID').value;
    var link = "/skills/" + idValue;
});

function updateTitleGeneratedLink(newTitle) {
    document.title = newTitle;
}

function generateLink(event) {
    var idInput = document.getElementById("inputID");
    var generatedLink = document.getElementById("generatedLink");

    var idValue = idInput.value;
    var link = "/skills/" + idValue;

    if (idValue === '') {
        generatedLink.href = link;
        generatedLink.textContent = 'Link to the list of skills';
        generatedLink.className = 'toggleButton';
    } else {
        generatedLink.href = link;
        generatedLink.textContent = 'Link to the selected skill with id ' + idValue;
        generatedLink.className = 'toggleButton';
    }

    if (idValue === '') {
        var newTitle = 'List of Skills';
        updateTitleGeneratedLink(newTitle);
    } else {
        var newTitle = 'Selected skill with id ' + idValue;
        updateTitleGeneratedLink(newTitle);
    }
    return false;
}

