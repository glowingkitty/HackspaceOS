function showAddKeyword() {
    document.getElementById('keyword_add').style.display = 'none'
    document.getElementById('keyword_save').style.display = 'inline-block'
    document.getElementById('keyword_input').style.display = 'inline-block'
    document.getElementById('keyword_input').focus()
    document.getElementById('keyword_input').select()
}

function saveKeyword() {
    document.getElementById('keyword_add').style.display = 'inline-block'
    document.getElementById('keyword_save').style.display = 'none'
    document.getElementById('keyword_input').style.display = 'none'

    if (document.getElementById('keyword_input').value && document.getElementById('keyword_input').value != '') {
        document.getElementById('keywords').innerHTML = document.getElementById('keywords').innerHTML + '<a href="#" onclick="enterSearch(this.innerText)" class="keyword">' + document.getElementById('keyword_input').value + '</a>'
        axios.get("/save?keyword=" + document.getElementById('keyword_input').value)
            .then(function () {
                document.getElementById('keyword_input').value = ''
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {});
    }
}