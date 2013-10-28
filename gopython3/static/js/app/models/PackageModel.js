define('app/models/PackageModel', [
    'underscore',
    'backbone'
], function(
    _,
    Backbone
){
    return Backbone.Model.extend({
        defaults: {
            url: '',
            name: '',
            version: '',
            status: 'pending',
            pypi: [],
            repo: {},
            issues: [],
            forks: [],
            pr: [],
            ci: {},
            comments: {}
        },

        baseUrl: '/api/v1/packages/',

        url: function(){
            if (this.get('id')) {
                return this.baseUrl + this.get('id') + '/';
            }
        },

        initialize: function(){
            this.on('change:status', this.fetchIfCompleted, this);
            this.fetchIfCompleted();
        },

        isCompleted: function(){
            return this.get('status') == 'success';
        },

        fetchIfCompleted: function(){
            console.log(this.isCompleted());
            if (this.isCompleted()) {
                this.fetch({
                    success: function(){
                        console.info('success', arguments);
                    }
                });
            }
        },

        getPython3Support: function(){
            var info;

            if (!this.isCompleted()) {
                return 'UNDEFINED'
            }

            info = this.toJSON();
            if (info.pypi && info.pypi.current && info.pypi.current.python3.length) {
                return 'SUPPORTED';
            }
            if (info.pypi && info.pypi.latest && info.pypi.latest.python3.length) {
                return 'SUPPORTED_IN_NEXT';
            }
            if (!_.isEmpty(info.forks)) {
                return 'SUPPORTED_PROBABLY';
            }
            return 'UNKNOWN';
        }
    });
});
