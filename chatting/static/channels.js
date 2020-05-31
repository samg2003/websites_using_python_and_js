document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        document.querySelector('form button').onclick = () => {
            const selection = document.querySelector('form input').value;
            socket.emit('add channel', {'selection': selection})
        };
    });
    socket.on ('display chan', data => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="/channels/${data["channelname"]}"> ${data["selection"]} </a>`;
        console.log(li.innerHTML);
        document.querySelector('#chatrooms').prepend(li);
    });
});
