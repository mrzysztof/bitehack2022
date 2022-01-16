var commentsRoot = document.querySelector("ytd-comments");
var comments = [];

function sendRequest(request){

    fetch('http:/127.0.0.1:8800/detect_and_replace', {

    // Declare what type of data we're sending
    headers: {
      'Content-Type': 'application/json'
    },

    // Specify the method
    method: 'POST',

    // A JSON payload
    body: JSON.stringify(request)
}).then(function (response) { // At this point, Flask has printed our JSON
    console.log('is?');
    return response.text();
}).then(function (text) {

    console.log('POST response: ');

    // Should be 'OK' if everything was successful
    console.log(text);
});
    // let xhr = new XMLHttpRequest();
    // let url = "http://127.0.0.1:8800/detect_and_replace";
    // xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // xhr.onreadystatechange = function () {
    //     console.log(xhr.responseText);
    //     if(xhr.readyState === 4) {
    //         //const response = JSON.parse(xhr.responseText);
    //         console.log(xhr.responseText);
    //     }
    // };
    // console.log(xhr);
    // xhr.send(request);
    // console.log(xhr);
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
sendRequest(request);

console.log("end");