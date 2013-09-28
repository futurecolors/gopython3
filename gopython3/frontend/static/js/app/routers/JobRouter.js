define('app/routers/JobRouter', [
    'marionette'
], function(
    Marionette
){
    return Marionette.AppRouter.extend({
        before: function(){
            this.options.App.startSubApp('Job');
        },

        appRoutes: {
            '': 'index'
        }
    });
});
