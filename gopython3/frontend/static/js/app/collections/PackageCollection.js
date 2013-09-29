define('app/collections/PackageCollection', [
    'app/collections/Collection',
    'app/models/PackageModel'
], function(
    Collection,
    PackageModel
){
    return Collection.extend({
        model: PackageModel,

        getProgress: function(){
            return this.where({status: 'completed'}).length / this.length;
        },

        getSupportStatus: function(){
            var supportStatuses,
                result = {};

            supportStatuses = _.map(
                this.where({status: 'completed'}),
                function(package){
                    return package.getPython3Support()
                }
            );
            _.each(['SUPPORTED', 'SUPPORTED_IN_NEXT', 'SUPPORTED_PROBABLY', 'UNKNOWN'], function(key){
                result[key] = _.filter(supportStatuses, function(value){return value == key}).length;
            });

            return result;
        }
    });
});
