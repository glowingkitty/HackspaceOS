// Noisebridge specific
function marryspeak(text) {
    axios.get('http://pegasus.noise:5000/?text=' + text)
        .then(function () {})
        .catch(function () {})
        .finally(function () {});
}