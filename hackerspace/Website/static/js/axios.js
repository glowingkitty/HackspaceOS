function request_html(parameter, replace_id, inner_OR_outer = 'inner') {
    axios.get("/get/?" + parameter, {
            cancelToken: new CancelToken(function executor(c) {
                // An executor function receives a cancel function as a parameter
                cancel_search = c;
            })
        })
        .then(function (response) {
            if (document.getElementById(replace_id) && response.data.html) {
                if (inner_OR_outer == 'inner') {
                    document.getElementById(replace_id).innerHTML = response.data.html
                } else if (inner_OR_outer == 'outer') {
                    document.getElementById(replace_id).outerHTML = response.data.html
                }

                // call extra functions if loading a new page
                parameter = parameter.replace(/__/g, '/')
                page = parameter.split('=')[1]
                if (page.includes('/')) {
                    onLoadFunctions(page)
                    history.pushState({}, response.data.page_name, page);
                    document.title = response.data.page_name
                }
            }

            // if message for marry, speak it out
            if (response.data.marryspeak) {
                for (message in response.data.marryspeak) {
                    marryspeak(response.data.marryspeak[message])
                }
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

function showMore(what, specific_selector) {
    axios.get("/load_more?what=" + what + '&from=' + document.getElementById('more_start_from' + specific_selector).value + '&specific_selector=' + specific_selector + '&origin=' + window.location.pathname)
        .then(function (response) {
            document.getElementById('more_start_from' + specific_selector).value = response.data.continue_from
            document.getElementById('next_results' + specific_selector).outerHTML = response.data.html
            if (response.data.more_results == false) {
                document.getElementById('button__show_more' + specific_selector).style.display = 'none'
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

function showMorePhotos() {
    axios.get('/load_more?what=photos&from=' + document.getElementById('more_start_from').value + '&type=' + document.getElementById('type').value)
        .then(function (response) {
            document.getElementById('more_start_from').value = response.data.continue_from
            document.getElementById('next_results').outerHTML = response.data.html
            if (response.data.more_results == false) {
                document.getElementById('button__show_more').style.display = 'none'
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

function getPhotos(button, type) {
    if (document.getElementById('photos_block')) {
        // if on photos page...
        if (window.location.href.includes('/photos')) {
            // deactivate other buttons
            document.getElementById('button__photo_latest').classList.remove('active')
            document.getElementById('button__photo_oldest').classList.remove('active')
            document.getElementById('button__photo_random').classList.remove('active')

            button.classList.add('active')

            document.getElementById('type').value = type
        }
        axios.get('/load_more?what=photos&from=0&type=' + type)
            .then(function (response) {
                if (window.location.href.includes('/photos')) {
                    document.getElementById('more_start_from').value = response.data.continue_from
                    document.getElementById('photos_block').innerHTML = response.data.html
                    if (response.data.more_results == false) {
                        document.getElementById('button__show_more').style.display = 'none'
                    }
                    location.hash = '#photos_block'
                } else {
                    document.getElementById('photos_block').innerHTML = response.data.html
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