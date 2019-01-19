var app = function() {
    Vue.config.devtools = true;
    var self = {};

    Vue.config.silent = false; // show all warnings

    self.load = function(start = 0) { //gets the first 10 public memos and also retrieves user data
        //generate url
        var pp = {
            start_idx: start
        };
        var url = "/get_notes" + "?" + $.param(pp);

        $.getJSON(url, function (data) {
            console.log(data)
            self.vue.notes_list = eval(data).reverse()
        })        
    };
    self.add = function() {

        var pp = {
            title: self.vue.noteTitle,
            body: self.vue.noteBody,

        };
        var url = "/post_note" + "?" + $.param(pp);
            var newElem = {"title": self.vue.noteTitle, "text": self.vue.noteBody}
            console.log(newElem)
            self.vue.notes_list.unshift(newElem)
            self.vue.noteTitle = ""
            self.vue.noteBody = ""
        $.getJSON(url, function (data) {

        })        
        
    };
    self.submit = function(){
        console.log("title: " + self.vue.noteTitle)
    }

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //booleans
            page_loaded: false,
            notes_list: [],
            noteTitle: "",
            noteBody: "",

        },
        methods: {
            add: self.add,
            submit: self.submit,
        }

    });

    //self.load();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
