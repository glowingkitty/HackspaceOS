function showAddKeyword() {
    document.getElementById('keyword_add').style.display = 'none'
    document.getElementById('keyword_save').style.display = 'inline-block'
    document.getElementById('keyword_input').style.display = 'inline-block'
    document.getElementById('keyword_input').focus()
    document.getElementById('keyword_input').select()
}

function saveKeyword(while_waiting_for_saving_str, rtl) {
    document.getElementById('keyword_add').style.display = 'inline-block'
    document.getElementById('keyword_save').style.display = 'none'
    document.getElementById('keyword_input').style.display = 'none'

    if (document.getElementById('keyword_input').value && document.getElementById('keyword_input').value != '') {
        document.getElementById('keywords').innerHTML = document.getElementById('keywords').innerHTML + '<a href="#" onclick="enterSearch(this.innerText,\'' + while_waiting_for_saving_str + '\',' + rtl + ')" class="keyword">' + document.getElementById('keyword_input').value + '<span class="button__remove_keyword" onclick="removeKeyword(event,this)"></span></a>'
        axios.get("/save?keyword=" + document.getElementById('keyword_input').value + '&origin=' + window.location.pathname)
            .then(function () {
                document.getElementById('keyword_input').value = ''
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {});
    }
}

function removeKeyword(event, element) {
    event.stopPropagation();
    axios.get("/remove?keyword=" + element.parentElement.innerText + '&origin=' + window.location.pathname)
        .then(function () {
            element.parentElement.outerHTML = ''
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {});
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

function nextMeetingTopic() {
    let current_meeting_topic_num = parseInt(document.getElementById('current_meeting_topic').value)
    let next_meeting_topic_num = current_meeting_topic_num + 1
    if (document.getElementById('meeting_topic_' + next_meeting_topic_num)) {
        document.getElementById('meeting_topic_' + current_meeting_topic_num).style.display = 'none'
        document.getElementById('meeting_topic_' + next_meeting_topic_num).style.display = 'inline-block'
        document.getElementById('current_meeting_topic').value = next_meeting_topic_num

        document.getElementById('previous_meeting_button').style.display = 'inline-block'
        let overnext_meeting_topic_num = current_meeting_topic_num + 2
        if (document.getElementById('meeting_topic_' + overnext_meeting_topic_num)) {
            document.getElementById('next_meeting_button').style.display = 'inline-block'
        } else {
            document.getElementById('next_meeting_button').style.display = 'none'
        }
    }
}

function previousMeetingTopic() {
    let current_meeting_topic_num = parseInt(document.getElementById('current_meeting_topic').value)
    let previous_meeting_topic_num = current_meeting_topic_num - 1
    if (document.getElementById('meeting_topic_' + previous_meeting_topic_num)) {
        document.getElementById('meeting_topic_' + current_meeting_topic_num).style.display = 'none'
        document.getElementById('meeting_topic_' + previous_meeting_topic_num).style.display = 'inline-block'
        document.getElementById('current_meeting_topic').value = previous_meeting_topic_num

        document.getElementById('next_meeting_button').style.display = 'inline-block'
        let overprevious_meeting_topic_num = current_meeting_topic_num - 2
        if (document.getElementById('meeting_topic_' + overprevious_meeting_topic_num)) {
            document.getElementById('previous_meeting_button').style.display = 'inline-block'
        } else {
            document.getElementById('previous_meeting_button').style.display = 'none'
        }
    }
}

function confirmMeetingOver() {
    // change to 'please wait' screen
    document.getElementById('meeting_over_heading').innerText = 'Saving the meeting...'
    document.getElementById('meeting_over_text').innerHTML = 'This might take a minute...'
    document.getElementById('meeting_over_buttons').style.display = 'none'
    document.getElementById('notes_embedded').style.display = 'none'
    document.getElementById('dark_overlay').onclick = function () {}

    // make request to server
    axios.get("/meeting/end")
        .then(function (response) {
            // load meeting page
            if (response.data.meeting_url)
                window.location = response.data.meeting_url
            else {
                alert(response.data.alert)
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {});
}