(() => {
  let goodImages
  let againImages

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

  const onLoad = () => {
    const div = document.createElement('div')
    div.id = 'visualFeedback'
    document.body.appendChild(div)
    // pycmd is still not initialized at this point
    setTimeout(() => {
      window.pycmd('audiovisualFeedback#files#images/good', (msg) => { goodImages = JSON.parse(msg) })
      window.pycmd('audiovisualFeedback#files#images/again', (msg) => { againImages = JSON.parse(msg) })
    }, 100)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)

  let timeout = null

  // ease: string "again" / "hard" / "good" / "easy"
  window.showVisualFeedback = (ease) => {
    const container = document.getElementById('visualFeedback')
    if (timeout) {
      clearTimeout(timeout)
    }

    const imgUrl = randomImageURL(ease)
    if (imgUrl === null) return

    const img = document.createElement('img')
    img.src = imgUrl
    container.appendChild(img)
    container.classList.add('visible')

    timeout = setTimeout((c) => {
      container.classList.remove('visible')
      container.removeChild(img)
    }, 200, ease)
  }
})()
