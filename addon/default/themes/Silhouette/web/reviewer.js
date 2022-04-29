(() => {
  let goodImages
  let againImages

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
  }

  const onLoad = () => {
    const div = document.createElement('div')
    div.id = 'visualFeedback'
    document.body.appendChild(div)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)
  retrieveImages()

  let timeout = null

  // ease: string "again" / "hard" / "good" / "easy"
  window.showVisualFeedback = (ease) => {
    const card = document.getElementById('qa')
    const container = document.getElementById('visualFeedback')
    if (timeout) {
      clearTimeout(timeout)
    }

    const imgUrl = randomImageURL(ease)
    if (imgUrl === null) return

    window.pycmd('audiovisualFeedback#disableShowAnswer')

    const img = document.createElement('img')
    img.src = imgUrl
    container.appendChild(img)
    container.classList.add('visible')
    card.classList.add('hidden')

    timeout = setTimeout((c) => {
      container.classList.remove('visible')
      card.classList.remove('hidden')
      container.removeChild(img)
      window.pycmd('audiovisualFeedback#enableShowAnswer')
    }, 1500, ease)
  }
})()
