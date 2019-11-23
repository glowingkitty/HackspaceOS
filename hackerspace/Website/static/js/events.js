function showFullDescription(description_name, button) {
    document.getElementById(description_name).classList.remove('text_box_max_height')
    button.style.display = 'none'
}

function showNewEventForm() {
    document.getElementById('event_name').value = document.getElementById('input_event_name').value
    document.getElementById('new_event_form').style.display = 'block'
    document.getElementById('what_event_block').style.display = 'none'
    document.getElementById('event_date').focus()
}

function checkForOverlappingEvents() {
    // check if all required fields are correctly filled out, if yes, check for overlapping events

    // check event date
    let event_date = document.getElementById('event_date').value
    if (event_date.length < 10) {
        return
    }
    if (event_date.replace(/[^-]/g, "").length < 2) {
        return
    }

    // check event time
    let event_time = document.getElementById('event_time').value
    if (event_time.length < 5) {
        return
    }
    if (event_time.replace(/[^:]/g, "").length < 1) {
        return
    }

    // check event duration
    let event_duration = document.getElementById('event_duration').value
    if (event_duration.length < 5) {
        return
    }
    if (event_duration.replace(/[^:]/g, "").length < 1) {
        return
    }

    // check event space
    let event_space = document.getElementById('event_space').value
    if (!event_space) {
        return
    }

    // make server request and check if overlapping events exist
    axios.get('/get/?what=event_overlap&date=' + event_date + '&time=' + event_time + '&duration=' + event_duration + '&space=' + event_space)
        .then(function (response) {
            if (response.data.int_overlapping_events > 0) {
                document.getElementById('overlapping_events').innerHTML = response.data.html
                document.getElementById('overlapping_events_section').style.display = 'block'
            } else {
                document.getElementById('overlapping_events_section').style.display = 'none'
                document.getElementById('overlapping_events').innerHTML = ''
            }
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });

}

function changeLocation(new_location) {
    if (new_location == 'other') {
        document.getElementById('location').value = ''
        document.getElementById('location_text').value = ''
        document.getElementById('location_text').style.display = 'block'
    } else {
        document.getElementById('location').value = new_location
        document.getElementById('location_text').style.display = 'none'
    }
}

function addRemoveHost(block, discourse_url) {
    if (document.getElementById('added_hosts').value.includes(discourse_url)) {
        block.outerHTML = ''
        document.getElementById('added_hosts').value = document.getElementById('added_hosts').value.replace(',' + discourse_url, '')
    } else {
        document.getElementById('hosts_preview').innerHTML = document.getElementById('hosts_preview').innerHTML + block.outerHTML
        block.outerHTML = ''
        document.getElementById('added_hosts').value = document.getElementById('added_hosts').value + ',' + discourse_url
    }

    if (document.getElementById('added_hosts').value != '') {
        document.getElementById('hosts_preview_block').style.display = 'block'
    } else {
        document.getElementById('hosts_preview_block').style.display = 'none'
    }
}