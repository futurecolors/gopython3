define('app/models/JobModel', [
    'backbone'
], function(Backbone){
    return Backbone.Model.extend({
        defaults: {
            url: '',
            status: '',
            packages: []
        },

        baseUrl: '/api/v1/jobs/',

        url: function(){
            var url;

            if (this.get('id')) {
                url = this.baseUrl + this.get('id') + '/';
            } else {
                url = this.baseUrl;
            }

            return url;
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
        },

        watch: function(){
            this.save().then(_.bind(this.tryToSave, this));
        },

        tryToSave: function(){
            var that = this;

            setTimeout(function(){
                that.fetch({
                    success: _.bind(that.onSave, that)
                });
            }, 5000);
        },

        onSave: function(){
            if (this.get('status') != 'completed') {
                this.tryToSave()
            }
        }
    });
});
