function search(query, while_waiting_string, rtl) {
    source.cancel()

    CancelToken = axios.CancelToken;
    source = CancelToken.source();
    if (query != undefined && query != '') {
        // show black block
        showOverlay()

        // show search bar active
        if (document.getElementById('search_bar').className == 'search_bar' || document.getElementById('search_bar').className == 'search_bar rtl') {
            document.getElementById('search_bar').classList.add('active')
        }

        if (rtl == true) {
            document.getElementById('search_results').innerHTML = '<div dir="rtl" align="right">' + while_waiting_string + '</div>'
        } else {
            document.getElementById('search_results').innerHTML = '<div>' + while_waiting_string + '</div>'
        }


        axios.get("/apis/hackspace_os/search?q=" + query, {
                cancelToken: new CancelToken(function executor(c) {
                    // An executor function receives a cancel function as a parameter
                    cancel_search = c;
                })
            })
            .then(function (response) {
                if (document.getElementById('search_input').value) {
                    // show results
                    document.getElementById('search_results').innerHTML = response.data.html
                }
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {
                // always executed
            });

    } else {
        document.getElementById('search_results').innerHTML = ''

        if (document.getElementById('search_bar').className == 'search_bar active' || document.getElementById('search_bar').className == 'search_bar rtl active') {
            document.getElementById('search_bar').classList.remove('active')
        }

        closeOverlays()
    }
}

function search_events(query) {
    if (!query || query == '') {
        document.getElementById('what_event_organize').style.marginTop = '20vh'
        document.getElementById('what_event_organize').style.marginBottom = '30vh'
        document.getElementById('existing_events_block').style.display = 'none'
        document.getElementById('continue_add_event_button').style.display = 'none'
    } else {
        document.getElementById('continue_add_event_button').style.display = 'inline-block'
        axios.get("/apis/hackspace_os/search?q=" + query + '&filter=events', {
                cancelToken: new CancelToken(function executor(c) {
                    // An executor function receives a cancel function as a parameter
                    cancel_search = c;
                })
            })
            .then(function (response) {
                // show results
                if (response.data.num_results > 0) {
                    document.getElementById('what_event_organize').style.marginTop = '0'
                    document.getElementById('what_event_organize').style.marginBottom = '0'
                    document.getElementById('existing_events_block').style.display = 'block'
                    document.getElementById('existing_events').innerHTML = response.data.html
                } else {
                    document.getElementById('what_event_organize').style.marginTop = '20vh'
                    document.getElementById('what_event_organize').style.marginBottom = '30vh'
                    document.getElementById('existing_events_block').style.display = 'none'
                }

            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {
                // always executed
            });
    }
}

function search_hosts(query) {
    axios.get("/apis/hackspace_os/search?q=" + query + '&filter=hosts', {
            cancelToken: new CancelToken(function executor(c) {
                // An executor function receives a cancel function as a parameter
                cancel_search = c;
            })
        })
        .then(function (response) {
            // show results
            if (response.data.num_results > 0) {
                document.getElementById('hosts_search_results').innerHTML = response.data.html
            } else {
                document.getElementById('hosts_search_results').innerHTML = ''
            }

        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

function enterSearch(text, while_waiting_string, rtl) {
    if (document.getElementById('search_input')) {
        document.getElementById('search_input').value = text
        search(document.getElementById('search_input').value, while_waiting_string, rtl)
    }
}

function clearSearch() {
    if (document.getElementById('search_input')) {
        document.getElementById('search_input').value = ''
        document.getElementById('search_results').innerHTML = ''

        if (document.getElementById('search_bar').className == 'search_bar active' || document.getElementById('search_bar').className == 'search_bar rtl active') {
            document.getElementById('search_bar').classList.remove('active')
        }
    }
}