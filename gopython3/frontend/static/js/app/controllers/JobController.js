define('app/controllers/JobController', [
    'backbone',
    'marionette',
    'app/layouts/JobLayout'
], function (
    Backbone,
    Marionette,
    JobLayout
) {
    return Marionette.Controller.extend(_.extend(
        // Initialization
        {
            initialize: function(){
                this.on('module:initialize', this.onInitialize, this);
                this.on('module:finalize', this.onFinalize, this);
            },

            onInitialize: function(){
                this.layout = new JobLayout();
                this.options.App.body.show(this.layout);
            },

            onFinalize: function(){
                this.layout.close();
            }
        },
        // Routs
        {
            index: function(){}
        }
    ));
});
