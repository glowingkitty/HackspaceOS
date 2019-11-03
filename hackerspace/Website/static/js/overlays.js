function showOverlayBlock() {
    document.getElementById('dark_overlay').classList.add('block')
    setTimeout(function () {
        document.getElementById('dark_overlay').classList.add('visible')
    }, 200)
}

function closeOverlays() {
    document.getElementById('dark_overlay').classList.remove('visible')
    setTimeout(function () {
        document.getElementById('dark_overlay').classList.remove('block')
    }, 200)
    enterSearch('')
}