var commentsRoot = document.querySelector("ytd-comments");
var comments = [];

function sendRequest(request){
    let xhr = new XMLHttpRequest();
    let url = "192.168.3.204:8800";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if(xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);
        }
    };
    xhr.send(request);
}

commentsRoot.querySelectorAll("ytd-comment-thread-renderer")
.forEach(node => comments.push(node));

comments = comments.map(node => node.querySelector("#content-text"));
let rawComments = comments.map(c => c.textContent);
let request = {"comments" : rawComments,
               "options" : {"maxOffensivity" : "neutral"}};

function update(){
  let currentComments = document.querySelectorAll("ytd-comments");
  //if()
}

console.log("end");