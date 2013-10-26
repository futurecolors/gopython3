define('app/modules/JobModule', [
    'underscore',
    'app/routers/JobRouter',
    'app/controllers/JobController'
], function(
    _,
    JobRouter,
    JobController
){
    return function(App){
        App.module('Job', {
            startWithParent: false,

            define: function(){
                var jobController = new JobController({
                    App: App
                });

                App.addInitializer(function(){
                    new JobRouter({
                        App: App,
                        controller: jobController
                    });
                });

                this.addInitializer(function(){
                    jobController.trigger('module:initialize');
                });
                this.addFinalizer(function(){
                    jobController.trigger('module:finalize');
                });
            }
        });
    };
});
