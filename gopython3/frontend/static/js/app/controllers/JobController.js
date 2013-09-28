define('app/controllers/JobController', [
    'backbone',
    'marionette',
    'app/layouts/JobLayout',
    'app/collections/PackageCollection',
    'app/views/JobFormView',
    'app/models/JobModel'
], function (
    Backbone,
    Marionette,
    JobLayout,
    PackageCollection,
    JobFormView,
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

                this.collection = new PackageCollection();
                this.model = new JobModel();
            },

            onFinalize: function(){
                this.layout.close();
                this.collection.remove();
                this.model.remove();
            }
        },
        // Routs
        {
            index: function(){
                var that = this;

                this.layout.ready(function(){
                    this.form.show(new JobFormView({
                        model: that.model,
                        collection: that.collection
                    }));
                });
            },

            job: function(){
                this.index();
            }
        }
    ));
});
