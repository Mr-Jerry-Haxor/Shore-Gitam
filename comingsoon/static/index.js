var objScrollTop = 0;
var scroll = 0;

$(window).on('load', function () {
    parallax(document.getElementById('level1'), -1.5, -4800);
    parallax(document.getElementById('level2'), -1, -2900);
    parallax(document.getElementById('level3'), -1.3, 200);
});

$('body').on('mousewheel DOMMouseScroll MozMousePixelScroll wheel', function (e) {
    handleScrollEvent(e);
});

$('body').on('touchstart touchmove', function (e) {
    handleTouchScrollEvent(e);
});

function handleScrollEvent(e) {
    if (e.originalEvent.wheelDelta !== undefined) {
        parallax(document.getElementById('level1'), -1.5, e.originalEvent.wheelDelta);
        parallax(document.getElementById('level2'), -1, e.originalEvent.wheelDelta);
        parallax(document.getElementById('level3'), -1.3, e.originalEvent.wheelDelta);
    } else if (e.originalEvent.deltaY !== undefined) {
        parallax(document.getElementById('level1'), -1.5, (e.originalEvent.deltaY * (-30)));
        parallax(document.getElementById('level2'), -1, (e.originalEvent.deltaY * (-30)));
        parallax(document.getElementById('level3'), -1.3, (e.originalEvent.deltaY * (-30)));
    }
}

function handleTouchScrollEvent(e) {
    var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
    var startY = touch.clientY;
    var lastY = startY;

    $(window).on('touchmove', function (event) {
        var touchMove = event.originalEvent.touches[0] || event.originalEvent.changedTouches[0];
        var currentY = touchMove.clientY;

        var deltaY = currentY - lastY;
        lastY = currentY;

        if (Math.abs(deltaY) > 10) {
            handleScrollEvent({ originalEvent: { deltaY: deltaY } });
        }
    });

    $(window).on('touchend', function () {
        $(window).off('touchmove touchend');
    });
}

function parallax(target, layer, scrollinit) {
    // Remaining parallax function remains the same as provided
    // ...
}

function append_gallery(column) {
    // Remaining append_gallery function remains the same as provided
    // ...
}
