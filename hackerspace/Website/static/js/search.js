function search(query) {
    axios.get("/search?q=" + query)
        .then(function (response) {
            if (query && query != '') {
                // show black block
                showOverlayBlock()

                // show search bar active
                if (document.getElementById('search_bar').className == 'search_bar') {
                    document.getElementById('search_bar').classList.add('active')
                }

                // show results
                document.getElementById('search_results').innerHTML = response.data.html


            } else {
                document.getElementById('search_results').innerHTML = ''

                if (document.getElementById('search_bar').className == 'search_bar active') {
                    document.getElementById('search_bar').classList.remove('active')
                }
                closeOverlays()
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}