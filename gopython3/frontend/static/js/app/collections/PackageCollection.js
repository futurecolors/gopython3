define('app/collections/PackageCollection', [
    'app/collections/Collection'
], function(
    Collection
){
    return Collection.extend({
        getProgress: function(){
            return this.where({status: 'compeleted'}).length / this.length;
        },

        getSupportStatus: function(){
            var supportStatuses,
                result = {};

            supportStatuses = _.map(
                this.where({status: 'compeleted'}),
                function(package){
                    return package.getPython3Support()
                }
            );
            _.each(['SUPPORTED', 'SUPPORTED_IN_NEXT', 'SUPPORTED_PROBABLY', 'UNSUPPORTED'], function(key){
                result[key] = _.filter(supportStatuses, function(value){return value == key}).length;
            });

            return result;
        }
    });
});
