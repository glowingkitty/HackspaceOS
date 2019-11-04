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

function startNewMeeting() {
    // show loading screen
    request_html('what=start_meeting', 'join_next_meeting', 'outer')

    // make request to start new meeting
    axios.get('/new?what=meeting')
        .then(function (response) {
            // if done, replace meeting placeholder with real meeting preview
            document.getElementById('current_meeting_block').outerHTML = response.data.html
        })
        .catch(function (error) {
            console.log(error)
        })
        .finally(function () {});
}