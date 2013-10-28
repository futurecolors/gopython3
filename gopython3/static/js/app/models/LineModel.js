define('app/models/LineModel', [
    'backbone',
    'app/models/PackageModel'
], function(Backbone, PackageModel){
    return Backbone.Model.extend({
        defaults: {
            is_failed: false
        },

        initialize: function(){
            this.setPackage();
            this.on('change:package', this.setPackage, this);
        },

        setPackage: function(){
            this.package = new PackageModel(this.get('package'))
        }
    });
});
