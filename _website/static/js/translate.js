function get_name_fields(name_input) {
    // request to server: get translation to all languages
    axios.get('/apis/hackspace_os/translate', {
            params: {
                'q': name_input
            }
        })
        .then(function (response) {
            // show fields for all languages
            for (language in response.data) {
                document.getElementById('event_name_' + language).value = response.data[language]
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

function translate_description(from_language, to_language) {
    // send server request
    if (document.getElementById('event_description_' + from_language).value) {
        axios.get('/apis/hackspace_os/translate', {
                params: {
                    'q': document.getElementById('event_description_' + from_language).value,
                    'language': to_language
                }
            })
            .then(function (response) {
                document.getElementById('event_description_' + to_language).value = response.data.text
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {
                // always executed
            });
    }
}

function save_language(to_language) {
    var CookieDate = new Date;
    CookieDate.setFullYear(CookieDate.getFullYear() + 1);
    document.cookie = 'lang=' + to_language + '; expires=' + CookieDate.toGMTString() + ';';
}