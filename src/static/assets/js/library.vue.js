(function(Vue) {
    "use strict";

    var initSelect = 'All categories...';

    new Vue({
        el: '#library',
        data: {
            items: [],
            cats: [initSelect],
            cat: initSelect,
            search: '',
        },

      created: function() {
        var self = this;
        this.$nextTick(function() {
          self.$refs.search.focus();
        });

        var url = '/api/library';
        this.$http.get(url).then(function(res) {
          res.json(res).then(function(result) {
            self.items = result;
            var cats = result.reduce(function(dic, item){
              dic[item.fields.category] = item.fields.category;
              return dic;
            }, {});


            for(var cat in cats) {
              self.cats.push(cat);
              self.cats.sort();
            }
          });
        });
      },

      methods: {
        filteredList: function() {
          var self = this;
          return self.items.filter(function(item) {
            var matchTitle = self.search === '' || item.fields.title.toLowerCase().includes(self.search.toLowerCase());

            var matchCat = self.cat === initSelect || item.fields.category == self.cat;
            return matchCat && matchTitle;
          })
        },
      },
    });
})(Vue);
