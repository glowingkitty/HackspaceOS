function openMenu() {
    document.getElementById('side_menu').classList.add('open')
}

function getPage(page) {
    request_html('what=' + page)
}