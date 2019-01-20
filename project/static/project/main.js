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


    self.testFunc = function(){
        var request = {
        }
        var url = "/testFunc" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
        })
    };

    self.accept = function(){
        var ev = -1
        if (self.vue.curr_event != -1)
            ev = self.vue.event_ids[self.vue.curr_event]

        var request = {
            "otherID": self.vue.suggested_usr_id,
             "eventID": ev,
        }
        var url = "/accept" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            self.vue.group = data.group
            if (data.group!=-1) 
            {
                alert("Hello! I am an alert box!!");
            }
            self.getNextMatch()
        })
    };

    self.decline = function(){
        var ev = -1
        if (self.vue.curr_event != -1)
            ev = self.vue.event_ids[self.vue.curr_event]

        var request = {
            "eventID": ev,
        }
        var url = "/decline" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            self.getNextMatch()
        })

    };

    self.getNextMatch = function(){
        var ev = -1
        if (self.vue.curr_event != -1)
            ev = self.vue.event_ids[self.vue.curr_event]

        var request = {
                "eventID": ev,
        }
        var url = "/getNextMatch" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            self.vue.suggested_usr_name =  data.suggested_usr_name
            self.vue.suggested_usr_id =  data.suggested_usr_id
        })
    };

    self.loadData = function(){
        var request = {
        }
        var url = "/loadData" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            $("#vue-div").show();
            console.log(data)
            self.vue.event_names = data.event_names
            self.vue.event_ids = data.event_ids
            self.vue.curr_event = data.curr_event
            self.getNextMatch()
            self.vue.logged_in = true
        })
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //booleans
            page_loaded: false,
            suggested_usr_name: "",
            suggested_usr_id: -1,
            logged_in: false,
            event_names: [],
            event_ids: [],
            curr_event: -1,
            group: -1,

        },
        methods: {
            add: self.add,
            accept: self.accept,
            decline: self.decline,
            testFunc: self.testFunc,
            getNextMatch: self.getNextMatch,
            loadData: self.loadData,
        }

    });

    //self.load();
    self.loadData()
    //self.getNextMatch()
    

    

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
