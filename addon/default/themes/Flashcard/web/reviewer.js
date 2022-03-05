(() => {
    window.addEventListener("load", () => {
        const div = document.createElement("div")
        div.id = "visualFeedback"
        document.body.appendChild(div)
    })

    let timeout = null
    
    // ease: string "again" / "hard" / "good" / "easy"
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

