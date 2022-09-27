module.exports = {
  devServer: {
    open: true,
    proxy: {
      '/api': {
        target: 'https://gcdll-back-gcdll.app.secoder.net', // 修改为你的Django服务器地址
        changOrigin: true,
        pathRewrite: {
          // '^/api': ''
        }
      }
    }
  }
}
