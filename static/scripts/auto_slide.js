function cycleBackgrounds() {
    var index = 0;

    let $imageEls = $('.container .slide');

    setInterval(function () {
        // Get the next index.  If at end, restart to the beginning.
        index = index + 1 < $imageEls.length ? index + 1 : 0;
        // Show the next image.
        $imageEls.eq(index).addClass('show');
        // Hide the previous image.
        $imageEls.eq(index - 1).removeClass('show');

        }, 4500);  // the time
    }

    $(function () {
    	cycleBackgrounds();
    });