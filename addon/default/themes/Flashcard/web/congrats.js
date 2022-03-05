(() => {
    const onLoad = () => {
        const div = document.createElement("div")
        div.id = "cat-container"
    
        const img = document.createElement("img")
        img.id = "cat-image"
        pycmd("audiovisualFeedback#randomFile#images/congrats", (src) => {
            img.src = src
            div.appendChild(img)
            document.body.insertBefore(div, document.body.firstChild)    
        })
    }

    if (document.readyState === "complete") {
        onLoad()
    } else {
        window.addEventListener("load", onLoad)
    }
})()