function openMenu() {
    showOverlay()
    document.getElementById('side_menu').classList.add('open')
}

function getPage(page) {
    closeOverlays()
    request_html('what=' + encodeURI(page.replace(/\//g, '__')), 'page_content', 'inner')
}