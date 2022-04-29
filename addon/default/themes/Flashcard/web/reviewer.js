(() => {
  const visualFeedbackDiv = () => {
    const div = document.createElement('div')
    div.classList.add('visualFeedback')
    document.body.appendChild(div)
    return div
  }

  const onLoad = () => {
    for (const pos of ['top', 'bottom', 'left', 'right']) {
      const div = visualFeedbackDiv()
      div.classList.add(pos)
    }
  }

  document.readyState === 'complete' ? onLoad() : window.addEventListener('load', onLoad)

  let timeout = null

  // ease: string "again" / "hard" / "good" / "easy"
  window.showVisualFeedback = (ease) => {
    const elems = document.getElementsByClassName('visualFeedback')
    if (timeout) {
      clearTimeout(timeout)
    }
    for (const elem of elems) {
      elem.classList.add(ease)
    }

    timeout = setTimeout((c) => {
      for (const elem of elems) {
        elem.classList.remove(c)
      }
    }, 300, ease)
  }
})()
