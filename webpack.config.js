var path = require('path');
var webpack = require('webpack');

module.exports = {
    context: __dirname + '/ecommerce/static',
    entry: {
        // Define apps and pages here. A single JS file will be output for each.
        course_admin_app: 'js/apps/course_admin_app',
        credit_checkout_app: 'js/apps/credit_checkout_app'
    },
    output: {
        path: __dirname + '/ecommerce/static/build',
        filename: '[name].js'
    },
    loaders: [
        { test: /\.html/, loader: 'raw' }
    ],
    resolve: {
        root: [
            __dirname + '/ecommerce/static',
            __dirname + '/ecommerce/static/js',
            __dirname + '/ecommerce/static/bower_components'
        ],
        extensions: ['', '.js', '.html'],
        alias: {
            'backbone': 'backbone/backbone',
            'backbone.relational': 'backbone-relational/backbone-relational',
            'backbone.route-filter': 'backbone-route-filter/backbone-route-filter',
            'backbone.stickit': 'backbone.stickit/backbone.stickit',
            'backbone.super': 'backbone-super/backbone-super/backbone-super',
            'backbone.validation': 'backbone-validation/dist/backbone-validation-amd',
            'bootstrap': 'bootstrap-sass/assets/javascripts/bootstrap',
            'bootstrap_accessibility': 'bootstrapaccessibilityplugin/plugins/js/bootstrap-accessibility',
            'datatables.net': 'datatables/media/js/jquery.dataTables',
            'dataTablesBootstrap': 'datatables/media/js/dataTables.bootstrap',
            'jquery': 'jquery/dist/jquery',
            'jquery-cookie': 'jquery-cookie/jquery.cookie',
            'moment': 'moment/moment',
            'requirejs': 'requirejs/require',
            'text': 'text/text',
            'underscore': 'underscore/underscore',
            'underscore.string': 'underscore.string/dist/underscore.string'
        }
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            names: ['common']
        })
    ]
}
