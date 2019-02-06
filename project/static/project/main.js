var app = function() {
    Vue.config.devtools = true;
    var self = {};

    Vue.config.silent = false; // show all warnings
    
    self.changeEvent = function(num, bool) {
        self.vue.edit_profile = false
        self.vue.curr_event = num
        if (self.vue.events[num].isIn)
            self.getNextMatch()
    }


    self.accept = function(){

        var request = {
            "eventID": self.vue.events[self.vue.curr_event].ID,
            "acceptedUser": self.vue.suggested_usr_id
        }
        var url = "/accept" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
            if(typeof data.group != "undefined") {
                self.vue.events[self.vue.curr_event].group = data.group
            }
            self.getNextMatch()
        })
    };

    self.decline = function(){
        var request = {
            "eventID": self.vue.events[self.vue.curr_event].ID
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
            self.vue.events = data.events
            if(data.events.length != 0)
                self.vue.curr_event = 0
            if(data.events.length != 0 && self.vue.events[0].isIn)
                self.getNextMatch()
 
        })
    };

    self.testFunc1 =function(){
        var request = {
        }
        var url = "/testFunc1" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
        })
    }

    self.testFunc2 =function(){
        var request = {
        }
        var url = "/testFunc2" + "?" + $.param(request);

        $.getJSON(url, function (data) {
            console.log(data)
        })
    }

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            //booleans
            page_loaded: true,
            edit_profile: true,
            suggested_usr_name: "",
            suggested_usr_id: -1,
            logged_in: true,
            curr_event: -1,
            events: [],
            userData: null,

        },
        methods: {
            accept: self.accept,
            decline: self.decline,
            getNextMatch: self.getNextMatch,
            loadData: self.loadData,
            changeEvent: self.changeEvent,
            testFunc1: self.testFunc1,
            testFunc2: self.testFunc2,
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
