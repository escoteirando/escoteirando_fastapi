const path = require("path");
const output_Dir = process.env.DOCKER_BUILD ? "/static" : path.resolve(__dirname, "../static")
module.exports = {
    outputDir: output_Dir,
    publicPath: "/f",
    // assetsDir: "../static/assets"
}
