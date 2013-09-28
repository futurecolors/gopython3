define('app/layouts/JobLayout', [
    'marionette',
    'app/views/GreetingView'
], function(
    Marionette,
    GreetingView
){
    return Marionette.Layout.extend({
        template: 'app/templates/layout.jade',

        initialize: function(){
        },

        regions: {
            greeting: '.js-greeting'
        },

        onRender: function(){
            this.greeting.show(new GreetingView());
        }
    });
});
