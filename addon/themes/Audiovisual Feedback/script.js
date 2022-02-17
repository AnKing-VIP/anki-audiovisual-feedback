(() => {
    let timeout = null
    
    window.showVisualFeedback = (ease) => {
        const elem = document.getElementById("visualFeedback")
        if (timeout) {
            clearTimeout(timeout)
        }
        elem.classList.add(ease)

        timeout = setTimeout((c) => {
            elem.classList.remove(c)
        }, 300, ease)
    }
})()

