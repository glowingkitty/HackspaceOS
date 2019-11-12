function showActiveTab(tab) {
    Array.prototype.forEach.call(document.getElementsByName('tabs'), function (tab) {
        // Do stuff here
        tab.style.display = 'none'
    });

    Array.prototype.forEach.call(document.getElementsByName('tab_heading'), function (heading) {
        // Do stuff here
        heading.classList.remove('active')
    });

    document.getElementById('tab__' + tab).style.display = 'block'
    document.getElementById('tab_heading__' + tab).classList.add('active')
}