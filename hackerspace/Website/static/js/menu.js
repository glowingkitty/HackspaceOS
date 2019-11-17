function openMenu() {
    showOverlay()
    document.getElementById('side_menu').classList.add('open')
}

function switchMenuSelected(menu_item_active) {
    const menu_headings = document.getElementsByClassName('menu_heading');

    Array.prototype.forEach.call(menu_headings, function (heading) {
        // Do stuff here
        heading.classList.remove('selected')
    });

    document.getElementById(menu_item_active).classList.add('selected')
}

function getPage(page, menu_item_active) {
    event.preventDefault()
    closeOverlays()
    clearSearch()
    request_html('what=' + encodeURI(page.replace(/\//g, '__')), 'page_content', 'inner')
    switchMenuSelected(menu_item_active)
    window.scrollTo(0, 0);
}