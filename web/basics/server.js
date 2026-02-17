const cluster = require("node:cluster")
const os = require("os")
const express = require("express")


const cpus = os.cpus().length
console.log(cpus)


if (cluster.isPrimary) {
    for (let i = 0; i < cpus; i++){
        cluster.fork();
    }
} else {
    const app = express()
    const PORT = 8000

    app.get("/", (req, res) => {
        return res.json({
            message: `Shek shak shok from ${process.pid}`
        })
    })

    app.listen(PORT, () => console.log(`Server at PORT ${PORT}`))
}