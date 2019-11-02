function check_if_in_space() {
    // check if website is opened in the hackerspace and define what to do
    axios.get('http://pegasus.noise:5000/')
        .then(function (response) {
            console.log(response)
            // show 'Say hello' button
            document.getElementById('cta_button').style.display = 'none'
            document.getElementById('cta_button_in_space').style.display = 'block'
        })
        .catch(function (response) {
            document.getElementById('cta_button').style.display = 'none'
            document.getElementById('cta_button_in_space').style.display = 'block'
        })
        .finally(function () {});
}

// Noisebridge specific
function marryspeak(text) {
    axios.get('http://pegasus.noise:5000/?text=' + text)
        .then(function () {})
        .catch(function () {})
        .finally(function () {});
}