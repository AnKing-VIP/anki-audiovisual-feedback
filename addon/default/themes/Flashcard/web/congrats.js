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

    document.readyState === "complete" ? onLoad() : window.addEventListener("load", onLoad)
})()