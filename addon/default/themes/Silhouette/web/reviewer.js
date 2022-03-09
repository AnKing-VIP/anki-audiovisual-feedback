(() => {
    let goodImages;
    let againImages;

    const randomImageURL = (ease) => {
        let array;
        if (ease === "good" || ease === "easy") {
            array = goodImages    
        } else {
            array = againImages
        }
        return array[Math.floor(Math.random() * array.length)]
    }

    const onLoad = () => {
        const div = document.createElement("div")
        div.id = "visualFeedback"
        document.body.appendChild(div)
        // pycmd is still not initialized at this point
        setTimeout(() => {
            pycmd("audiovisualFeedback#files#images/good", (msg) => {goodImages = JSON.parse(msg)})
            pycmd("audiovisualFeedback#files#images/again", (msg) => {againImages = JSON.parse(msg)})        
        }, 100)
    }

    document.readyState === "complete" ? onLoad() : window.addEventListener("load", onLoad)


    let timeout = null
    
    // ease: string "again" / "hard" / "good" / "easy"
    window.showVisualFeedback = (ease) => {
        const card = document.getElementById("qa")
        const container = document.getElementById("visualFeedback")
        if (timeout) {
            clearTimeout(timeout)
        }
        pycmd("audiovisualFeedback#disableShowAnswer")
        
        const img = document.createElement("img")
        img.src = randomImageURL(ease)
        container.appendChild(img)
        container.classList.add("visible")
        card.classList.add("hidden")

        // TODO: is it possible to prevent going to answer side?
        timeout = setTimeout((c) => {
            container.classList.remove("visible")
            card.classList.remove("hidden")
            container.removeChild(img)
            pycmd("audiovisualFeedback#enableShowAnswer")
        }, 1500, ease)
    }
})()

