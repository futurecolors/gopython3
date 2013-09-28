define('app/views/GreetingView', [
    'marionette'
], function(Marionette){
    return Marionette.ItemView.extend({
        template: 'app/templates/greeting.jade'
    });
});
