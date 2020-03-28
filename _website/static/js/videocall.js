function load_videocall(room_name, domain) {
    const options = {
        roomName: room_name,
        width: '100%',
        height: 500,
        parentNode: document.getElementById('videocall')
    };
    const api = new JitsiMeetExternalAPI(domain, options);
}