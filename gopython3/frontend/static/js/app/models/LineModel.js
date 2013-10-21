define('app/models/LineModel', [
    'backbone',
    'app/models/PackageModel'
], function(Backbone, PackageModel){
    return Backbone.Model.extend({
        defaults: {
            package: null,
            is_failed: false
        },

        initialize: function(){
            this.on('change:package', this.setPackage, this);
        },

        setPackage: function(){
            this.package = new PackageModel(this.get('package'))
        }
    });
});
