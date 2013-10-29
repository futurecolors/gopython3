define('app/collections/LineCollection', [
    'app/collections/Collection',
    'app/models/LineModel'
], function(
    Collection,
    LineModel
){
    return Collection.extend({
        model: LineModel,

        getProgress: function(){
            return this.filter(function(line){
                return line.get('is_failed') || (line.package && line.package.get('status') == 'success');
            }).length / this.length;
        },

        getSupportStatus: function(){
            var result = {
                    SUPPORTED: 0,
                    SUPPORTED_IN_NEXT: 0,
                    SUPPORTED_PROBABLY: 0,
                    UNKNOWN: 0
                };

            this.each(function(line){
                result[line.package.getPython3Support()]++;
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
