define('app/models/JobModel', [
    'backbone'
], function(Backbone){
    return Backbone.Model.extend({
        defaults: {
            url: '',
            status: '',
            packages: []
        },

        baseUrl: 'http://python3.apiary.io/api/v1/jobs/',

        url: function(){
            if (this.get('id')) {
                return this.baseUrl + this.get('id') + '/';
            } else {
                return this.baseUrl;
            }
        },

        initialize: function(){
            this.on('change:url', this.setId, this);
        },

        setId: function(){
            var id,
                urlParts;

            urlParts = this.get('url').split('/');
            id = urlParts.length > 2 ? parseInt(urlParts[urlParts.length - 2]) : null;

            this.set({id: id});
        }
    });
});
