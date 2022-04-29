(() => {
  let goodImages
  let againImages
  let startImages

  let feedbackTimeout = null
  let waitingForStartImages = false

  function randomImageURL (array) {
    if (array.length === 0) return null
    return array[Math.floor(Math.random() * array.length)]
  }

  // Wait for pycmd to initialize
  function retrieveImages () {
    if (typeof pycmd === 'undefined') {
      setTimeout(retrieveImages, 10)
      return
    }
    window.pycmd('audiovisualFeedback#files#images/good', (msg) => { goodImages = JSON.parse(msg) })
    window.pycmd('audiovisualFeedback#files#images/again', (msg) => { againImages = JSON.parse(msg) })
    window.pycmd('audiovisualFeedback#files#images/start', (msg) => {
      startImages = JSON.parse(msg)
      if (waitingForStartImages) window.avfReviewStart()
    })
  }

  function onLoad () {
    const div = document.createElement('div')
    div.id = 'visualFeedback'
    document.body.appendChild(div)
  }

  function showImage (array) {
    const container = document.getElementById('visualFeedback')
    if (feedbackTimeout) {
      clearTimeout(feedbackTimeout)
    }

    const imgUrl = randomImageURL(array)
    if (imgUrl === null) return

    const img = document.createElement('img')
    img.src = imgUrl
    container.appendChild(img)
    container.classList.add('visible')

    feedbackTimeout = setTimeout((c) => {
      container.classList.remove('visible')
      container.removeChild(img)
    }, 200)
  }

  window.showVisualFeedback = (ease) => {
    const array = ease === 'good' || ease === 'easy' ? goodImages : againImages
    showImage(array)
  }

  window.avfReviewStart = () => {
    if (typeof startImages === 'undefined') {
      waitingForStartImages = true
      return
    }
    showImage(startImages)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)
  retrieveImages()
})()
