
var player = "";

function DrawSnakeBody(canvas, array) {
    for (var i = 0; i < array.length; i++) { 
         DrawSquare(canvas, array[i], "rgb(50, 200, 50)");
    }
}

function DrawApple(canvas, apple) {
    DrawSquare(canvas, apple, "rgb(50, 50, 200)")
}

function DrawSquare(canvas, point, colour) {
    var context = canvas.getContext("2d");
    context.fillStyle = colour;
    context.fillRect(point.x * 10, point.y * 10, 10, 10);
}

function DrawGameOver() {
    var canvas = document.getElementById("snake_field");
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.font = "20px Arial";
    context.fillStyle = "fuchsia";
    context.fillText("Game Over", 100, 100);
}

function RenderEverything(snakes, apple) {
    var canvas = document.getElementById("snake_field");
    var ccontext = canvas.getContext("2d");
    ccontext.clearRect(0, 0, canvas.width, canvas.height);
    DrawApple(canvas, apple);
    snakes.forEach(function(snake){
        DrawSnakeBody(canvas, snake.body);
    });
}

function FieldUpdate(msg) {
    RenderEverything(msg.snakes, msg.apple);
}


namespace = '/test';
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
        
document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
        socket.emit("turn right", {data:player});
    }
    if (event.key === "ArrowLeft") {
        socket.emit("turn left", {data:player});
    }
    if (event.key === "ArrowUp") {
        socket.emit("turn up", {data:player});
    }
    if (event.key === "ArrowDown") {
        socket.emit("turn down", {data:player});
    }
    if (event.key === " ") {
        socket.emit("toggle pause", {data:player});
    }
    if (event.key === "R") {
        socket.emit("restart_game", {data:player});
    }
}, false);


function Main() {
    socket.on("field_change", FieldUpdate);

    socket.on("prompt username", function() {
        player = prompt("Enter your username:");
        socket.emit('new player', {data: player});
    });

    socket.on("username is already taken", function() {
        var player = prompt("Username is already taken. Try another one:");
        socket.emit('new player', {data: player});
    })

    socket.on("game_over", DrawGameOver);
}

document.body.onload = Main;
