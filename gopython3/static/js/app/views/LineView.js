define('app/views/LineView', [
    'marionette',
    'moment'
], function(
    Marionette,
    moment
){
    return Marionette.ItemView.extend({
        template: 'app/templates/line.jade',

        initialize: function(){
            this.model.on('change', this.render, this)
            this.model.package.on('change', this.render, this)
        },

        serializeData: function(){
            var python3Support;

            python3Support = this.model.package.getPython3Support();

            return {
                lineInfo: this.model.toJSON(),
                packageInfo: this.model.package.toJSON(),
                isCompleted: this.model.package.isCompleted(),
                python3Support: python3Support,
                moment: moment,
                isSupported: python3Support == 'SUPPORTED' || python3Support == 'SUPPORTED_IN_NEXT'
            };
        }
    });
});
