define('app/views/JobStatusView', [
    'marionette'
], function(Marionette){
    return Marionette.ItemView.extend({
        template: 'app/templates/status.jade',

        initialize: function(){
            this.collection.on('change reset', this.render, this)
        },

        serializeData: function(){
            return {
                progress: this.collection.getProgress()  * 100,
                support: this.collection.getSupportStatus()
            };
        }
    });
});
