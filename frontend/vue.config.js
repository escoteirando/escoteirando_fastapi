module.exports = {
  "outputDir": process.cwd()+"/static",
  "publicPath": "/f",
  "transpileDependencies": [
    "vuetify"
  ],
  configureWebpack: {
    devtool: 'source-map'
  }
}