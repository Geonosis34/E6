console.clear()

const chatBox = document.querySelector('#chat-box')
chatBox.addEventListener('submit', e => {
  e.preventDefault()
  const messageInp = document.querySelector('#message')
  let message = messageInp.value
  messageInp.value = ''
  if (message && message !== '') ws(message)
  message = ''
})

function getCookie(name) {
  let matches = document.cookie.match(
    new RegExp(
      '(?:^|; )' +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') +
        '=([^;]*)'
    )
  )
  return matches ? decodeURIComponent(matches[1]) : undefined
}
const board = document.querySelector('#board')
function scrolltoend() {
  board.scrollTo({ top: board.scrollHeight, behavior: 'smooth' })
}

const roomName = JSON.parse(document.getElementById('room-name').textContent)
const user = JSON.parse(document.querySelector('#user').textContent)
const userId = JSON.parse(document.querySelector('#user-id').textContent)
const roomId = JSON.parse(document.querySelector('#room-id').textContent)

const token = getCookie('csrftoken')
wsUrl = `ws://${window.location.host}/ws/chat/${roomName.toLowerCase()}/`

let socket = new WebSocket(wsUrl)

socket.onopen = function (e) {
  console.log('[open] Connection established')
  console.log('Sending to server')

  console.log(e)
}

socket.onmessage = function (event) {
  const resp = JSON.parse(event.data)
  console.log(`[message] Data received from server: ${event.data}`)
  const url = `http://${window.location.host}/api/messages/`
  fetch(url)
    .then(response => response.json())
    .then(data => console.log(data[data.length - 1]))

  appendMessage(resp)
}

socket.onclose = function (event) {
  if (event.wasClean) {
    console.log(
      `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
    )
  } else {
    console.log('[close] Connection died')
  }
}

socket.onerror = function (error) {
  console.log(`[error] ${error.message}`)
}

function ws(message) {
  console.log('Message Submitted')
  url = `/api/messages/`
  const data = {
    message: message,
    sender: userId,
    room: roomId,
  }

  console.log(message)
  socket.send(JSON.stringify(data))
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]')
        .value,
    },
    credentials: 'same-origin',
    body: JSON.stringify(data),
  })
}

function appendMessage(resp) {
  const msgBox = document.createElement('div')
  const msgBody = document.createElement('div')
  msgBox.classList.add('card', 'm-3')
  resp.sender_id === userId
    ? msgBox.classList.add('align-self-end', 'bg-secondary')
    : msgBox.classList.add('align-self-start', 'bg-light')
  const rm = resp.room_members

  const avatar = document.getElementById(`${resp.sender_id}`).firstElementChild
    .src

  const msg = `
    <div class="card-header">
      <img class="avatar" src="${avatar}" alt="${rm[resp.sender_id]}">
      <span class="timestamp">on ${resp.time}</span>
    </div>
    <div class="card-body">
      <h4 class="card-title">${
        resp.sender_id === userId ? 'You' : rm[resp.sender_id]
      }</h4>
      <p class="card-text"> ${resp.message}
      </p>
    </div>`

  msgBody.innerHTML = msg
  msgBox.appendChild(msgBody)
  board.appendChild(msgBox)


  scrolltoend()
}

scrolltoend()
