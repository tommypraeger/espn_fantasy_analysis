const path = require('path');

module.exports = {
  entry: './app/static/js/index.js',
  output: {
    path: path.join(__dirname, 'app/static'),
    filename: 'bundle.js',
  },
  watch: true,
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      } 
    ]
  },
  devServer: {
    contentBase: path.join(__dirname, 'app'),
    compress: true,
    port: 8000,
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
};
