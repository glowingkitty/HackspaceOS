function showOverlay(open_overlay = null) {
    document.getElementById('dark_overlay').classList.add('block')
    setTimeout(function () {
        document.getElementById('dark_overlay').classList.add('visible')
    }, 200)

    if (open_overlay) {
        document.getElementById(open_overlay + '_overlay').style.display = 'block'
    }

}

function closeOverlays() {
    let overlay_blocks = document.getElementsByClassName('overlay_block')
    for (block in overlay_blocks) {
        if (overlay_blocks[block].style) {
            overlay_blocks[block].style.display = 'none'
        }

    }
    document.getElementById('side_menu').classList.remove('open')
    document.getElementById('dark_overlay').classList.remove('visible')
    setTimeout(function () {
        document.getElementById('dark_overlay').classList.remove('block')
    }, 200)
}