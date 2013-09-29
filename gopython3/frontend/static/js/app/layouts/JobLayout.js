define('app/layouts/JobLayout', [
    'marionette',
    'app/views/GreetingView'
], function(
    Marionette,
    GreetingView
){
    return Marionette.Layout.extend({
        template: 'app/templates/layout.jade',

        initialize: function(){},

        regions: {
            greeting: '.js-greeting',
            form: '.js-form',
            status: '.js-status',
            packages: '.js-packages'
        },

        onRender: function(){
            this.greeting.show(new GreetingView());
        }
    });
});
