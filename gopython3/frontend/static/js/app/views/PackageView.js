define('app/views/PackageView', [
    'marionette',
    'moment'
], function(
    Marionette,
    moment
){
    return Marionette.ItemView.extend({
        template: 'app/templates/package.jade',

        initialize: function(){
            this.model.on('change', this.render, this)
        },

        serializeData: function(){
            return {
                packageInfo: this.model.toJSON(),
                isCompleted: this.model.isCompleted(),
                python3Support: this.model.getPython3Support(),
                moment: moment,
                blockClass: {
                    SUPPORTED: 'panel-success',
                    SUPPORTED_IN_NEXT: 'panel-success',
                    SUPPORTED_PROBABLY: 'panel-warning',
                    UNSUPPORTED: 'panel-danger'
                }[this.model.getPython3Support()]
            };
        }
    });
});
