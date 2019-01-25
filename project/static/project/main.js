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
        var ev = -1
        if(!self.vue.curr_type) {
            if(self.vue.curr_event != -1)
                ev = self.vue.event_ids[self.vue.curr_event]
        }
        else {
            if(self.vue.curr_event != -1)
                ev = self.vue.my_event_ids[self.vue.curr_event]
        }

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
        if(!self.vue.curr_type) {
            if(self.vue.curr_event != -1)
                ev = self.vue.event_ids[self.vue.curr_event]
        }
        else {
            if(self.vue.curr_event != -1)
                ev = self.vue.my_event_ids[self.vue.curr_event]
        }

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
        if(!self.vue.curr_type) {
            if(self.vue.curr_event != -1)
                ev = self.vue.event_ids[self.vue.curr_event]
        }
        else {
            if(self.vue.curr_event != -1)
                ev = self.vue.my_event_ids[self.vue.curr_event]
        }

        var request = {
                "eventID": ev,
                "type": self.vue.curr_type
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
            event_names: [],
            event_ids: [],
            my_event_names: [],
            my_event_ids: [],
            curr_event: -1,
            curr_type: false,
            group: -1,
            my_events: [],

        },
        methods: {
            add: self.add,
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
