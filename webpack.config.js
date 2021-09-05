const webpack = require('webpack');
const config = {
    entry:  __dirname + '/frontend/index.js',
    output: {
        path: __dirname + '/backend/flask_dir/static/dist/',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },

    module: {
        rules: [
            {
                test: /\.(js|jsx)?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            }
        ]


    },

};
module.exports = config;