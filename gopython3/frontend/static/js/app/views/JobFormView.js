define('app/views/JobFormView', [
    'marionette'
], function(Marionette){
    return Marionette.ItemView.extend({
        events: {
            'submit .js-form': 'onFormSubmit'
        },

        template: 'app/templates/form.jade',

        initialize: function(){
            this.model.on('change:url', function(){
                Backbone.history.navigate(this.get('url').slice(location.href.length), {trigger: true});
            });
        },

        serializeData: function(){
            return {
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
