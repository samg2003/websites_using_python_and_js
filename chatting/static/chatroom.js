document.addEventListener('DOMContentLoaded', () => {
    const request = new XMLHttpRequest();
    request.open("POST", "/messagesload");
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        localStorage.setItem("channelname", data["channelname"])
        for (let i=0; i<data["message"].length; i++) {
            const li = document.createElement('li');
            const message = data["message"][i];
            li.innerHTML = `<strong style="font-size:20px">${message["username"]}</strong> : <span class="mx-4"><big>${message["selection"]}</big></span> <small>${message["time"]}</small>`;
            li.ondblclick = function(){
              this.remove();
            };
            document.querySelector('#messages').prepend(li);
        }
    };
    request.send();
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        document.querySelector('button').onclick = function () {
            const selection = document.querySelector('input').value;
            this.form.reset();
            socket.emit('add message', {'selection': selection});
        };
    });
    socket.on ('display mess', data => {
        if (data["channelname"] === localStorage.channelname) {
            const li = document.createElement('li');
            li.innerHTML = `<strong style="font-size:20px">${data["username"]}</strong> : <span class="mx-4"><big>${data["selection"]}</big></span> <small>${data["time"]}</small>`;
            li.ondblclick = function(){
              this.remove();
            };
            document.querySelector('#messages').prepend(li);
        }
    });
});
