define('app/App', [
    'backbone',
    'marionette',
    'app/modules/JobModule'
], function(
    Backbone,
    Marionette,
    JobModule
){
    var App = new Marionette.Application();

    // Инициализация
    App.addRegions({
        body: '.js-body'
    });
    App.on('initialize:after', function(){
        JobModule(App);
    });
    App.on('initialize:after', function(){
        Backbone.history.start({pushState: true});
    });

    // Действие при старте модуля (вызывается из роутинга)
    App.startSubApp = function(moduleName){
        var currentApp = App.module(moduleName);

        if (App.currentApp === currentApp) {
            return;
        }
        if (App.currentApp) {
            App.currentApp.stop();
        }
        App.currentApp = currentApp;
        currentApp.start();
    };

    return App;
});
