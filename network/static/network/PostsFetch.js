// TODO: Fetch a certain amount of posts.
let emptyHeart = "../../static/network/heart-empty.png"
let filledHeart = "../../static/network/heart-filled.png"

document.getElementById("post--creation--form").onsubmit = (e) => makePost(e)

function fetchPosts() {
    console.log("Fetching posts")
    fetch("/posts")
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            let feed = document.querySelector("#posts--feed")
            feed.innerHTML = ""
            posts.forEach(post => {
                let postDiv = designPost(post)
                feed.appendChild(postDiv)
            })
        })
}

function makePost(e) {
    e.preventDefault()
    console.log("Submitting Form")
    let csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value
    let message_box = document.querySelector("#id_message")
    fetch("/posts", {
        method: "POST",
        headers: {"X-CSRFToken": csrf_token},
        body: JSON.stringify({
            message: message_box.value
        })
    })
        .then(() => fetchPosts())
}


// Creates a styled div with the post content
function designPost(post) {
    let postDiv = document.createElement('div')
    postDiv.classList.add('post')
    postDiv.setAttribute('id', `post-#${post.id}`)

    let usernameTitle = document.createElement('h4')
    usernameTitle.innerHTML = "@" + post.poster

    let messageDiv = document.createElement('div')
    messageDiv.classList.add('text-success')
    messageDiv.innerHTML = post.message.replace(/(\r\n|\r|\n)/g, "<br>")

    let dateDiv = document.createElement('div')
    dateDiv.innerHTML = "Posted on " + post.timestamp

    let likeBtn = document.createElement('div')
    let btnImg = document.createElement('img')
    btnImg.classList.add('like-button')
    btnImg.src = emptyHeart;
    likeBtn.appendChild(btnImg)
    btnImg.onclick = () => toggleLike(post.id)

    let likeCount = document.createElement('span')
    likeCount.classList.add('like--count--display')
    likeCount.innerHTML = post.like_count
    likeBtn.appendChild(likeCount)

    postDiv.append(usernameTitle, messageDiv, dateDiv, likeBtn)

    return postDiv
}

function toggleLike(post_id){
    fetch('/')
}