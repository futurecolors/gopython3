define('app/collections/PackageCollection', [
    'app/collections/Collection'
], function(
    Collection
){
    return Collection.extend({
        getProgress: function(){
            return this.where({status: 'compeleted'}).length / this.length;
        }
    });
});
