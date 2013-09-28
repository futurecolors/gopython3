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
            ci: {},
            comments: {}
        },

        baseUrl: 'http://python3.apiary.io/api/v1/packages/',

        url: function(){
            if (this.get('id')) {
                return this.baseUrl + this.get('id') + '/';
            }
        },

        getPython3Support: function(){
            var info = this.toJSON();

            if (info.pypi && info.pypi.current && info.pypi.current.python3) {
                return 'SUPPORTED';
            }
            if (info.pypi && info.pypi.latest && info.pypi.latest.python3) {
                return 'SUPPORTED_IN_NEXT';
            }
            if (!_.isEmpty(info.forks)) {
                return 'SUPPORTED_PROBABLY';
            }
            return 'UNSUPPORTED';
        }
    });
});
