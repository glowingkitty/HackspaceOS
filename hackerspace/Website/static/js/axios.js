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

function showMore(what) {
    axios.get("/load_more?what=" + what + '&from=' + document.getElementById('more_start_from').value)
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