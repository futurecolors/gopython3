define('app/collections/Collection', [
    'backbone'
], function(Backbone){
    return Backbone.Collection.extend({
        url: function(){
            var query;

            query = this.getQuery() || require.s.contexts._.config.urlArgs;

            return this.getBaseUrl() + '?' + query;
        },

        getBaseUrl: function(){
            return this.apiUrl;
        },

        getQuery: function(){},

        parse: function(response){
            return response['items'];
        }
    });
});
