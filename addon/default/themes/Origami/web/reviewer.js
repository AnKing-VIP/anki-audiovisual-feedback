(() => {
  let goodImages
  let againImages
  let startImages

  let waitingForStartImages = false

  // May return null
  const randomImageURL = (ease) => {
    let array
    if (ease === 'good' || ease === 'easy') {
      array = goodImages
    } else {
      array = againImages
    }
    if (array.length === 0) return null

    return array[Math.floor(Math.random() * array.length)]
  }

  // Wait for pycmd to initialize
  const retrieveImages = () => {
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

  const onLoad = () => {
    const div = document.createElement('div')
    div.id = 'visualFeedback'
    document.body.appendChild(div)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)
  retrieveImages()

  let timeout = null

  function showImage (array) {
    const container = document.getElementById('visualFeedback')
    if (timeout) {
      clearTimeout(timeout)
    }

    const imgUrl = randomImageURL(array)
    if (imgUrl === null) return

    const img = document.createElement('img')
    img.src = imgUrl
    container.appendChild(img)
    container.classList.add('visible')

    timeout = setTimeout(() => {
      container.classList.remove('visible')
      container.removeChild(img)
    }, 200)
  }

  // ease: string "again" / "hard" / "good" / "easy"
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
})()
