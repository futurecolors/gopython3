define('app/views/JobStatusView', [
    'marionette'
], function(Marionette){
    return Marionette.ItemView.extend({
        template: 'app/templates/job.status.jade',

        initialize: function(){
            this.collection.on('change', this.render, this)
        }
    });
});
