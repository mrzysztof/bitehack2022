var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const commentsRoot = document.querySelector("ytd-comments");
var commentElements = [];
var lastSize = 0;
commentsRoot.querySelectorAll("ytd-comment-thread-renderer")
.forEach(node => commentElements.push(node));
commentElements = commentElements.map(node => node.querySelector("#content-text"));
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

function sendRequest(request){
    let xhr = new XMLHttpRequest();
    let url = "http://127.0.0.1:8800";
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

function extractRawComments(directCommentElements){
    return directCommentElements.map(c => c.textContent);
}

let rawComments = extractRawComments(commentElements);
let request = {"comments" : rawComments,
               "options" : {"maxOffensivity" : "neutral"}};
  
function update(){
  let currentCommentElements = commentsRoot.querySelectorAll("ytd-comment-thread-renderer");

  if(currentCommentElements.length >= lastSize){
    let currentCommentElementsArr = [];
    let newCommentElements = [];
    currentCommentElements.forEach(ce => currentCommentElementsArr.push(ce));
    currentCommentElementsArr = currentCommentElements.map(node => node.querySelector("#content-text"));

    for(let i = lastSize; i < currentCommentElementsArr.length; i++){
        newCommentElements.push(currentCommentElements.childNodes[i]);
    }
     
    request(extractRawComments(newCommentElements));
  }
}
let xhr = new XMLHttpRequest();
let url = "http://127.0.0.1:8800";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = function () {
    if(xhr.readyState === 4 && xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        console.log(response);      
    }
};
xhr.send(request);    // let url = "http://127.0.0.1:8800/detect_and_replace";
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
>>>>>>> a0911899105f6c6cc4b8b96c5ddc001b5e78ebf5
}

function extractRawComments(directCommentElements){
    return directCommentElements.map(c => c.textContent);
}

let rawComments = extractRawComments(commentElements);
let request = {"comments" : rawComments,
               "options" : {"maxOffensivity" : "neutral"}};
<<<<<<< HEAD
  
function update(){
  let currentCommentElements = commentsRoot.querySelectorAll("ytd-comment-thread-renderer");

  if(currentCommentElements.length >= lastSize){
    let currentCommentElementsArr = [];
    let newCommentElements = [];
    currentCommentElements.forEach(ce => currentCommentElementsArr.push(ce));
    currentCommentElementsArr = currentCommentElements.map(node => node.querySelector("#content-text"));
=======
function update(){
  let currentComments = document.querySelectorAll("ytd-comments");
  //if()
}
sendRequest(request);
>>>>>>> a0911899105f6c6cc4b8b96c5ddc001b5e78ebf5

    for(let i = lastSize; i < currentCommentElementsArr.length; i++){
        newCommentElements.push(currentCommentElements.childNodes[i]);
    }
     
    request(extractRawComments(newCommentElements));
  }
}
