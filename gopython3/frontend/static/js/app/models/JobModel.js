define('app/models/JobModel', [
    'backbone'
], function(Backbone){
    var currentInstance;

    return Backbone.Model.extend({
        defaults: {
            url: '',
            status: '',
            packages: [],
            requirements: ''
        },

        baseUrl: '/api/v1/jobs/',

        initialize: function(){
            this.on('change:url', this.setId, this);
        },

        url: function(){
            var url;

            if (this.get('id')) {
                url = this.baseUrl + this.get('id') + '/';
            } else {
                url = this.baseUrl;
            }

            return url;
        },

        setId: function(){
            var id,
                urlParts;

            urlParts = this.get('url').split('/');
            id = urlParts.length > 2 ? parseInt(urlParts[urlParts.length - 2]) : null;

            this.set({id: id});
        },

        watch: function(){
            this.save().then(_.bind(this.tryToSave, this));
        },

        tryToSave: function(){
            currentInstance = this;

            setTimeout(function(){
                currentInstance.fetch({
                    success: _.bind(currentInstance.onSave, currentInstance)
                });
            }, 5000);
        },

        onSave: function(){
            if (this.get('status') != 'completed' && this.get('packages').length > 0) {
                this.tryToSave()
            }
        }
    });
});
