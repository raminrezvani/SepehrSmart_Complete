const { defineConfig } = require('@vue/cli-service')
// const webpack = require("webpack");




module.exports = {
  configureWebpack: {
    devtool: 'source-map'  // Ensure source maps are generated
  }
};

// module.exports = {
//   devServer: {
//     host: '0.0.0.0', // Bind to all network interfaces
//     port: 8080, // The port your app runs on (adjust as needed)
//     disableHostCheck: true, // Disable host check to allow access from other devices
//   },
//   configureWebpack: {
//     devtool: 'source-map',  // Ensure source maps are generated for debugging
//   }
// };








// module.exports = defineConfig({
//   transpileDependencies: true,
//   // configureWebpack: {
//   //   devtool: 'source-map'
//   // }
//   // configureWebpack: {
//   //   plugins: [new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)]
//   // },
// })
