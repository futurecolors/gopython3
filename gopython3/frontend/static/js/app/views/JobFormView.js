define('app/views/JobFormView', [
    'marionette'
], function(Marionette){
    return Marionette.ItemView.extend({
        events: {
            'submit .js-form': 'onFormSubmit'
        },

        template: 'app/templates/form.jade',

        initialize: function(){
            this.model.on('change:id', function(){
                Backbone.history.navigate('jobs/' + this.get('id') + '/', {trigger: true});
            });
            this.collection.on('reset', this.render, this);
        },

        serializeData: function(){
            return {
                job: this.model.toJSON(),
                isEmpty: this.collection.length == 0
            };
        },

        onFormSubmit: function(e){
            var data = {};

            e.preventDefault();

            _.each(this.$('.js-form').serializeArray(), function(param){
                data[param.name] = param.value;
            });

            this.model.set(data);
            this.model.save();
        }
    });
});
