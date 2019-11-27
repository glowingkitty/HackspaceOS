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
        document.getElementById('location_button_other').classList.remove('not_active')
        document.getElementById('location_button_hackerspace').classList.add('not_active')

        document.getElementById('location').value = ''
        document.getElementById('location_text').value = ''
        document.getElementById('location_text').style.display = 'block'
    } else {
        document.getElementById('location_button_other').classList.add('not_active')
        document.getElementById('location_button_hackerspace').classList.remove('not_active')

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

        document.getElementById('search_host_input').value = ''
        document.getElementById('hosts_search_results').innerHTML = ''
    }

    if (document.getElementById('added_hosts').value != '') {
        document.getElementById('hosts_preview_block').style.display = 'block'
    } else {
        document.getElementById('hosts_preview_block').style.display = 'none'
    }
}

function ask_who_welcomes_people(new_value) {
    if (new_value == 'large') {
        document.getElementById('who_welcomes_people').style.display = 'block'
    } else {
        document.getElementById('who_welcomes_people').style.display = 'none'
    }
}

function isFileImage(file) {
    const acceptedImageTypes = ['image/jpeg', 'image/png'];

    return file && acceptedImageTypes.includes(file['type'])
}

function checkFileTooLarge(file) {
    const fsize = file.size;
    const file_size = Math.round((fsize / 1024));
    // The size of the file. 
    if (file_size >= 2048) {
        return true
    }
}

function new_event(url_image) {

    // create event
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.get("/new", {
            params: {
                'what': 'event',
                'name': document.getElementById('event_name').value,
                'date': document.getElementById('event_date').value,
                'time': document.getElementById('event_time').value,
                'duration': document.getElementById('event_duration').value,
                'space': document.getElementById('event_space').value,
                'photo': url_image,
                'description': document.getElementById('event_description').value,
                'location': document.getElementById('event_location').value,
                'guilde': document.getElementById('event_guilde').value,
                'hosts': document.getElementById('added_hosts').value,
                'repeating': document.getElementById('repeating').value,
                'repeating_up_to': document.getElementById('upto_date').value,
                'volunteers': document.getElementById('event_volunteers').value,
                'expected_crowd': document.getElementById('event_expected_crowd').value,
                'event_welcomer': document.getElementById('event_welcomer').value,
            }
        })
        .then(function (response) {
            getPage(response.data.url_next)
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            // always executed
        });

}

function publish_event() {
    // check if fields are missing
    if (!document.getElementById('event_name').value) {
        return alert('"Name" is missing')
    }
    if (!document.getElementById('event_date').value) {
        return alert('"Date" is missing')
    }
    if (!document.getElementById('event_time').value) {
        return alert('"Time" is missing')
    }
    if (!document.getElementById('event_duration').value) {
        return alert('"Duration" is missing')
    }
    if (!document.getElementById('event_space').value) {
        return alert('"Space" is missing')
    }
    if (!document.getElementById('event_description').value) {
        return alert('"Description" is missing')
    }
    if (!document.getElementById('event_location').value) {
        return alert('"Location" is missing')
    }
    if (!document.getElementById('added_hosts').value) {
        return alert('Who is organizing the event? Select one or more hosts.')
    }
    if (!document.getElementById('event_volunteers').value) {
        return alert('Select if you need volunteers or not.')
    }
    if (!document.getElementById('event_expected_crowd').value) {
        return alert('Select how many people you expect.')
    }
    if (document.getElementById('event_expected_crowd').value == 'large' && !document.getElementById('event_welcomer').value) {
        return alert('Field missing. Who is welcoming people at the door?')
    }


    // upload image
    let url_image = null
    let input = document.getElementById('event_photo')
    if (input.files && input.files[0]) {
        var files = input.files

        if (isFileImage(files[0]) == false) {
            return alert('Please upload an JPG or PNG file')
        }

        if (checkFileTooLarge(files[0]) == true) {
            return alert('Maximum image size is 2MB')
        }

        let data = new FormData();

        for (var i = 0; i < files.length; i++) {
            let file = files.item(i);
            data.append('images[' + i + ']', file, file.name);
        }

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.post('/upload/event-image', data, {
                headers: {
                    'content-type': 'multipart/form-data'
                },
                cancelToken: source.token,
            })
            .then(function (response) {
                url_image = response.data.url_image
                new_event(url_image)
            })
            .catch(function (error) {
                console.log(error);
            })
            .finally(function () {
                // always executed
            });

    } else {
        new_event(url_image)
    }


}