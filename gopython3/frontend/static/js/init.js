(function () {
    require.config({
        paths: {
            backbone: 'libs/backbone',
            underscore: 'libs/underscore',
            jquery: 'libs/jquery',
            marionette: 'libs/backbone.marionette',
            'backbone.wreqr': 'libs/backbone.wreqr',
            'backbone.babysitter': 'libs/backbone.babysitter',
            'backbone.routefilter': 'libs/backbone.routefilter',
            text: 'libs/require.text',
            jade: 'libs/jade',
            moment: 'libs/moment',
            'jquery.form': 'libs/jquery.form'
        },
        shim: {
            jquery: {
                exports: 'jQuery'
            },
            underscore: {
                exports: '_'
            },
            backbone: {
                deps: ['jquery', 'underscore'],
                exports: 'Backbone'
            },
            marionette: {
                deps: ['jquery', 'underscore', 'backbone', 'backbone.routefilter'],
                exports: 'Marionette'
            },
            'jquery.form': {
                deps: ['jquery']
            }
        },
        waitSeconds: 60,
        urlArgs: "bust=" +  (new Date()).getTime()
    });

    var initBootstrap = function(){
        require(['../bootstrap/js/bootstrap']);
    };

    var initTemplates = function(_, Marionette, jade){
        Marionette.TemplateCache.get = function(templateName){
            var that = this,
                df = new $.Deferred(),
                cachedTemplate = this.templateCaches[templateName];

            if (cachedTemplate) {
                df.resolve(cachedTemplate);
            } else {
                require(['text!' + templateName], function(templateText){
                    cachedTemplate = jade.compile(templateText);
                    that.templateCaches[templateName] = cachedTemplate;
                    df.resolve(cachedTemplate);
                });
            }

            return df;
        };
        Marionette.Renderer.render = function(template, data){
            var df = new $.Deferred();

            Marionette.TemplateCache.get(template).then(function(cachedTemplate){
                df.resolve(cachedTemplate(data));
            });

            return df;
        };
        Marionette.ItemView.prototype.render = function(){
            this.isClosed = false;

            this.triggerMethod('before:render', this);
            this.triggerMethod('item:before:render', this);

            var data = this.serializeData();
            data = this.mixinTemplateHelpers(data);

            var template = this.getTemplate();
            var htmlDf = Marionette.Renderer.render(template, data);

            htmlDf.then(_.bind(function(html){
                this.$el.html(html);
                this._isRendered = true;

                this.bindUIElements();

                this.triggerMethod('render', this);
                this.triggerMethod('item:rendered', this);
            }, this));

            return this;
        };
        Marionette.CompositeView.prototype.render = function(){
            this.isRendered = true;
            this.isClosed = false;
            this.resetItemViewContainer();

            this.triggerBeforeRender();
            var htmlDf = this.renderModel();
            htmlDf.done(_.bind(function(html){
                this.$el.html(html);
                // the ui bindings is done here and not at the end of render since they
                // will not be available until after the model is rendered, but should be
                // available before the collection is rendered.
                this.bindUIElements();
                this.triggerMethod("composite:model:rendered");

                this._renderChildren();

                this.triggerMethod("composite:rendered");
                this.triggerRendered();
            }, this));

            return this;
        };
        Marionette.Layout.prototype.ready = function(callback){
            if (this._isRendered) {
                callback.call(this);
            } else {
                this.once('render', _.bind(function(){
                    callback.call(this);
                }, this))
            }
        };
    };

    var initLinks = function($, Backbone){
        $(function(){
            $(document).on('click', 'a[href]', function(e){
                e.preventDefault();

                Backbone.history.navigate($(e.target).attr('href'), {trigger: true});
            });
        });
    };

    define([
        'jquery',
        'underscore',
        'backbone',
        'marionette',
        'jade',
        'app/App'
    ], function (
        $,
        _,
        Backbone,
        Marionette,
        jade,
        App
    ) {
        initBootstrap();
        initTemplates(_, Marionette, jade);
        initLinks($, Backbone);

        App.start();
    });
})();
