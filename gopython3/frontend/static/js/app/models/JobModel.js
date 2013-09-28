define('app/models/JobModel', [
    'backbone'
], function(Backbone){
    return Backbone.Model.extend({
        defaults: {
            url: ''
        },

        url: 'http://python3.apiary.io/api/v1/jobs/'
    });
});
