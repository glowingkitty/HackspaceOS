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

            // if getting events, inform about next events
            if (response.data.events_in_5_minutes) {
                for (event_name in response.data.events_in_5_minutes) {
                    marryspeak(response.data.events_in_5_minutes[event_name] + ' is starting in 5 minnutes')
                }
            }
            if (response.data.events_in_30_minutes) {
                for (event_name in response.data.events_in_30_minutes) {
                    marryspeak(response.data.events_in_30_minutes[event_name] + ' is starting in 30 minnutes')
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