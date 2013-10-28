define('app/controllers/JobController', [
    'backbone',
    'marionette',
    'app/layouts/JobLayout',
    'app/collections/LineCollection',
    'app/views/JobFormView',
    'app/views/JobStatusView',
    'app/views/LineListView',
    'app/models/JobModel'
], function (
    Backbone,
    Marionette,
    JobLayout,
    LineCollection,
    JobFormView,
    JobStatusView,
    LineListView,
    JobModel
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

            createDataStorages: function(createNew){
                if (!this.model || !this.collection || createNew) {
                    this.collection = new LineCollection();
                    this.model = new JobModel();
                    this.model.collection = this.collection;
                }
            },

            onFinalize: function(){
                this.layout.close();

                if (this.collection) {
                    this.collection.remove();
                }
                if (this.model) {
                    this.model.remove();
                }
            }
        },
        // Routs
        {
            index: function(){
                var that = this;

                this.createDataStorages(true);
                this.layout.ready(function(){
                    this.form.show(new JobFormView({
                        model: that.model
                    }));
                    this.status.close();
                    this.packages.close();
                });
            },

            job: function(id){
                var that = this;

                this.createDataStorages();
                this.model.set({
                    id: id
                });
                this.model.fetch();

                this.layout.ready(function(){
                    this.status.show(new JobStatusView({
                        collection: that.collection
                    }));
                    this.packages.show(new LineListView({
                        collection: that.collection
                    }));
                });
            }
        }
    ));
});
