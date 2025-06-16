const express = require("express")

const app = express()
const PORT = 8000


app.get("/", (req, res) => {
    return res.json({
        message: `Shek shak shok from ${process.pid}`
    })
})

app.listen(PORT, () => console.log(`Server on PORT: ${PORT}`))