function request_html(parameter, replace_id, inner_OR_outer = 'inner') {
    axios.get("/get/?" + parameter, {
            cancelToken: new CancelToken(function executor(c) {
                // An executor function receives a cancel function as a parameter
                cancel_search = c;
            })
        })
        .then(function (response) {
            if (response.data.html) {
                if (inner_OR_outer == 'inner') {
                    document.getElementById(replace_id).innerHTML = response.data.html
                } else if (inner_OR_outer == 'outer') {
                    document.getElementById(replace_id).outerHTML = response.data.html
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