(() => {
  let images
  let container
  let image

  // Includes from, doesn't include to
  const randomInteger = (from, to) => {
    return Math.floor(Math.random() * (to - from)) + from
  }

  const randomImageURL = () => {
    if (images.length === 0) return null
    return images[randomInteger(0, images.length)]
  }

  const onLoad = () => {
    container = document.createElement('div')
    container.id = 'visualFeedback'
    document.body.appendChild(container)

    image = document.createElement('img')
    container.appendChild(image)

    // pycmd is still not initialized at this point
    setTimeout(() => {
      window.pycmd('audiovisualFeedback#files#images', (msg) => { images = JSON.parse(msg) })
    }, 100)
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)

  let timeout = null

  // ease: string "again" / "hard" / "good" / "easy"
  window.showVisualFeedback = (ease) => {
    if (ease !== 'good' && ease !== 'easy') { return }

    if (timeout) {
      clearTimeout(timeout)
    }

    const imgUrl = randomImageURL(ease)
    if (imgUrl === null) return

    image.src = imgUrl
    container.classList.add('visible')

    timeout = setTimeout((c) => {
      container.classList.remove('visible')
    }, 2000)
  }
})()
