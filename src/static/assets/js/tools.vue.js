(function(Vue) {
    "use strict";

    new Vue({
        el: '#tools',
        data: {
            items: [],
            search: '',
        },

      created: function() {
        var self = this;
        var url = '/api/tools';
        this.$http.get(url).then(function(res) {
          res.json(res).then(function(result) {
            self.items = result;
          });
        });
      },

      methods: {
        filteredList: function() {
          var self = this;
          console.log("=================");
          if (self.search === '') {
            console.log(self.items);
            return self.items;
          }
          return self.items.filter(function(item) {
            return item.fields.title.toLowerCase().includes(self.search.toLowerCase());
          })
        },
      },
    });
})(Vue);

