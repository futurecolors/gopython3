define('app/views/LineListView', [
    'marionette',
    'app/views/LineView'
], function(
    Marionette,
    LineView
){
    return Marionette.CollectionView.extend({
        itemView: LineView
    });
});
