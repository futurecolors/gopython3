define('app/controllers/JobController', [
    'backbone',
    'marionette'
], function (
    Backbone,
    Marionette
) {
    return Marionette.Controller.extend(_.extend(
        // Initialization
        {
            initialize: function(){
                this.on('module:initialize', this.onInitialize, this);
                this.on('module:finalize', this.onFinalize, this);
            },

            onInitialize: function(){s
            },

            onFinalize: function(){
            }
        },
        // Routs
        {
        }
    ));
});
