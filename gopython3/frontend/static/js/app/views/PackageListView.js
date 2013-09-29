define('app/views/PackageListView', [
    'marionette',
    'app/views/PackageView'
], function(
    Marionette,
    PackageView
){
    return Marionette.CollectionView.extend({
        itemView: PackageView
    });
});
