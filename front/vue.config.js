module.exports = {
  devServer: {
    proxy: 'http://localhost:8090',
    port: 8091,
  },
  configureWebpack: {
    devtool: 'source-map'
  },
}
