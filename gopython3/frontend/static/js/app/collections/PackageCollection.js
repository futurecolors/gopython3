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
        },

        getMessage: function(){
            var counters,
                message;

            counters = this.getSupportStatus();
            if (counters.SUPPORTED_PROBABLY == 0 && counters.UNKNOWN == 0) {
                message = 'Migration to python 3 is quite possible :-)'
            } else if (counters.SUPPORTED + counters.SUPPORTED_IN_NEXT > counters.SUPPORTED_PROBABLY + counters.UNKNOWN) {
                message = 'Worth a try &hellip;';
            } else {
                message = 'Better luck next time :-(';
            }

            return message;
        }
    });
});
