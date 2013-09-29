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
            var python3Support;

            python3Support = this.model.getPython3Support();

            return {
                packageInfo: this.model.toJSON(),
                isCompleted: this.model.isCompleted(),
                python3Support: python3Support,
                moment: moment,
                isSupported: python3Support == 'SUPPORTED' || python3Support == 'SUPPORTED_IN_NEXT'
            };
        }
    });
});
