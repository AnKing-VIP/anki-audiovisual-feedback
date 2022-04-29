(() => {
  let images
  let container
  let image

  const randomImageURL = () => {
    if (images.length === 0) return null
    return images[Math.floor(Math.random() * images.length)]
  }

  // Wait for pycmd to initialize
  const retrieveImages = () => {
    if (typeof pycmd === 'undefined') {
      setTimeout(retrieveImages, 10)
      return
    }
    window.pycmd('audiovisualFeedback#files#images', (msg) => { images = JSON.parse(msg) })
  }

  const onLoad = () => {
    container = document.createElement('div')
    container.id = 'visualFeedback'
    document.body.appendChild(container)

    image = document.createElement('img')
    container.appendChild(image)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)
  retrieveImages()

  let timeout = null

  function showImage () {
    if (timeout) {
      clearTimeout(timeout)
    }

    const imgUrl = randomImageURL()
    if (imgUrl === null) return
    image.src = imgUrl
    container.classList.add('visible')

    timeout = setTimeout((c) => {
      container.classList.remove('visible')
    }, 2000)
  }

  // ease: string "again" / "hard" / "good" / "easy"
  window.showVisualFeedback = (ease) => {
    if (ease !== 'good' && ease !== 'easy') { return }
    showImage()
  }
})()
