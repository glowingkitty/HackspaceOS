function openMenu() {
    document.getElementById('side_menu').classList.add('open')
}

function getPage(page) {
    request_html('what=' + encodeURI(page.replace(/\//g, '__')), 'page_content', 'inner')
}