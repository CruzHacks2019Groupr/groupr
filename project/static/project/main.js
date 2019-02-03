var app = function() {
    Vue.config.devtools = true;
    var self = {};

    Vue.config.silent = false; // show all warnings
    
    self.changeEvent = function(num, bool) {
        self.vue.curr_event = num
        self.vue.curr_type = bool
        self.getNextMatch()
    }


    self.testFunc = function(){
        var request = {
        }
        var url = "/testFunc" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
        })
    };

    self.accept = function(){

        var request = {
        }
        var url = "/accept" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            self.getNextMatch()
        })
    };

    self.decline = function(){
        var request = {
        }
        var url = "/decline" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            self.getNextMatch()
        })

    };

    self.getNextMatch = function(){

        var request = {
            "eventID": self.vue.events[self.vue.curr_event].ID
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
        $("#vue-div").show();
        $.getJSON(url, function (data) {
            
            console.log(data)
            self.vue.curr_event = data.curr_event
            self.vue.my_events = data.my_events
            self.vue.events = data.events
            self.vue.curr_type = data.curr_type
            if(!data.curr_type)
                self.getNextMatch()
 
        })
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //booleans
            page_loaded: true,
            suggested_usr_name: "",
            suggested_usr_id: -1,
            logged_in: true,
            curr_event: -1,
            curr_type: false,
            my_events: [],
            events: [],

        },
        methods: {
            accept: self.accept,
            decline: self.decline,
            testFunc: self.testFunc,
            getNextMatch: self.getNextMatch,
            loadData: self.loadData,
            changeEvent: self.changeEvent,
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
