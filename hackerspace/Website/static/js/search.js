function search(query) {
    source.cancel()

    CancelToken = axios.CancelToken;
    source = CancelToken.source();
    if (query != undefined && query != '') {

        axios.get("/search?q=" + query, {
                cancelToken: new CancelToken(function executor(c) {
                    // An executor function receives a cancel function as a parameter
                    cancel_search = c;
                })
            })
            .then(function (response) {

                // show black block
                showOverlayBlock()

                // show search bar active
                if (document.getElementById('search_bar').className == 'search_bar') {
                    document.getElementById('search_bar').classList.add('active')
                }

                // show results
                document.getElementById('search_results').innerHTML = response.data.html

            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {
                // always executed
            });

    } else {
        document.getElementById('search_results').innerHTML = ''

        if (document.getElementById('search_bar').className == 'search_bar active') {
            document.getElementById('search_bar').classList.remove('active')
        }
        closeOverlays()
    }
}

function enterSearch(text) {
    document.getElementById('search_input').value = text
    search(search_input.value)
}