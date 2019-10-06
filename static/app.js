let button, wordList, shapeList

document.addEventListener('DOMContentLoaded', onDocumentLoaded)

function onDocumentLoaded() {
  button = document.querySelector('#refreshList')
  wordList = document.querySelector('#topWordsList')
  shapeList = document.querySelector('#topShapesList')

  refreshTopK()

  button.addEventListener('click', onRefreshClicked)
}

function onRefreshClicked() {
  refreshTopK()
}

function refreshTopK() {
  refreshTopKShapes()
  refreshTopKWords()
}

async function refreshTopKWords() {
  let response = await fetch('words')
  let words = await response.json()

  wordList.textContent = ""
  words
    .map(entry => `${entry.word} (${entry.count})`)
    .forEach(s => {
      let li = document.createElement("li")
      li.textContent = s
      wordList.appendChild(li)
    })
}

async function refreshTopKShapes() {
  let response = await fetch('shapes')
  let shapes = await response.json()

  shapeList.textContent = ""
  shapes
    .map(entry => `${entry.shape} (${entry.count})`)
    .forEach(s => {
      let li = document.createElement("li")
      li.textContent = s
      shapeList.appendChild(li)
    })
}
