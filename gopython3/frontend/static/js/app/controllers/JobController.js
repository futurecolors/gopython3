define('app/controllers/JobController', [
    'backbone',
    'marionette',
    'app/layouts/JobLayout',
    'app/collections/PackageCollection',
    'app/views/JobFormView',
    'app/views/JobStatusView',
    'app/views/PackageListView',
    'app/models/JobModel'
], function (
    Backbone,
    Marionette,
    JobLayout,
    PackageCollection,
    JobFormView,
    JobStatusView,
    PackageListView,
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
                    this.collection = new PackageCollection();
                    this.model = new JobModel();
                    this.model.on('change:packages', function(){
                        this.collection.reset(this.model.get('packages'));
                    }, this)
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
                    this.packages.show(new PackageListView({
                        collection: that.collection
                    }));
                });
            }
        }
    ));
});
