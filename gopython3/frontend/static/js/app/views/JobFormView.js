define('app/views/JobFormView', [
    'marionette'
], function(
    Marionette
){
    return Marionette.ItemView.extend({
        events: {
            'submit .js-form': 'onFormSubmit',
            'change .js-requirements': 'setRequirementsHeight',
            'keyup .js-requirements': 'setRequirementsHeight'
        },

        template: 'app/templates/form.jade',

        initialize: function(){
            this.model.on('change:id', function(){
                Backbone.history.navigate('jobs/' + this.get('id') + '/', {trigger: true});
            });
        },

        serializeData: function(){
            return {
                job: this.model.toJSON()
            };
        },

        onFormSubmit: function(e){
            var data = {};

            e.preventDefault();

            _.each(this.$('.js-form').serializeArray(), function(param){
                data[param.name] = param.value;
            });

            if (this.model.id) {
                this.model.id = null;
            }
            delete this.model.attributes.id;
            this.model.set(data);
            this.model.watch();
        },

        setRequirementsHeight: function(){
            var $requirements,
                incomeRowCount,
                rowCount,
                height;

            $requirements = this.$('.js-requirements');
            incomeRowCount = $requirements.val().split('\n').length;
            rowCount = incomeRowCount > 4 ? 4 : incomeRowCount;
            height = 20 * rowCount;

            $requirements.attr('style', 'height: ' + (height + 12) + 'px !important');
            this.$('.js-submit').height(height - 2);
        }
    });
});
