function openMenu() {
    document.getElementById('side_menu').classList.add('open')
}

function getPage(page) {
    request_html('what=' + encodeURI(page.replace('/', '00')), 'page_content', 'inner')
}