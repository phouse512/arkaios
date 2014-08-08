/*(function ($) {
    var UpdateList, defaultOptions, __bind, size;
    
    
    __bind = function (fn, me) {
        return function () {
            return fn.apply(me, arguments);
        };
    };

    // Plugin default options.
    defaultOptions = {
        defaultId: 'selective_update_'
    };
    

    UpdateList = (function (options) {
        console.log('new class...');
       
        //I think this is the constructor?
        function UpdateList(handler, options) {
            options = options || {};
            this.handler = handler;
            console.log(this.handler);

            // Plugin variables.
            this.size = 0;

            // Extend default options.
            $.extend(true, this, defaultOptions, options);
        
            // Bind methods.
            this.update = __bind(this.update, this);
            this.template = __bind(this.template, this); 
            console.log('creating class instance')
        };

        // Method for updating the plugins options.
        UpdateList.prototype.update = function (options) {
            console.log("made it to the update section");

            //$.extend(true, this, options);
        };

        // Example API function.
        UpdateList.prototype.template = function (data) {
            console.log("template section");
        };

        return UpdateList;
    })();
/*
    UpdateList.prototype = {
        template: function() {
            console.log('updateList.template function call');
        },
        update: function() {
            console.log('updateList.update function call');
        }
    }

    $.fn.updatelist = function (operation, data) {
        console.log("begin execution");
        // Create a updateList instance if not available.
        /*if (!this.updateListInstance) {
            this.updateListInstance = new UpdateList(this, operation, data);
        } else {
            this.updateListance.template(data);
        }
        

        return this.each(function() {
            console.log("werd");
            var item = $(this), instance = item.data('updateList');
            console.log(instance);
            if(!instance) {
                // create plugin instance and save it in data
                item.data('updateList', new UpdateList(this));
            } else {
                instance.template(operation);
                // if instance already created call method
                //if(typeof opt === 'string') {
                    //instance.template(data)
                
            }
        });
        // Display items (if hidden) and return jQuery object to maintain chainability.
        //return this.show();
    }
}(jQuery)); */

(function($){
    // custom select class


    defaultOptions = {
        defaultId: 'selective_update_'
    };

    function UpdateList(item, options) {
        this.options = $.extend(defaultOptions, options);
        this.item = $(item);
        this.init();
    }
    UpdateList.prototype = {
        init: function() {
            console.log('initiation');
        },
        template: function(template) {
            this.template = template
        },
        update: function(newArray) {
            console.log('update');

            idList = new Array(newArray.length);
            console.log("length: " + newArray[0].length);
            for(var i=0; i < newArray[0].length; i++){
                console.log(newArray[0][i].id);
                idList.push(parseInt(newArray[0][i].id));
            }

            //console.log(idList);

            $("li").each(function(){
                //console.log(parseInt($(this).attr("id")));

                //console.log($.inArray(parseInt($(this).attr("id")), idList));

                if($.inArray(parseInt($(this).attr("id")), idList) >= 0){
                    console.log('in');
                } else {
                    //console.log('out');
                }

            });
            //scan through current, if current not in new
                // delete
                //if current is in new, remove from new
            // add remaining new
        }
    }

    // jQuery plugin interface
    $.fn.updateList = function(opt) {
        // slice arguments to leave only arguments after function name
        var args = Array.prototype.slice.call(arguments, 1);
        return this.each(function() {
            var item = $(this), instance = item.data('UpdateList');
            if(!instance) {
                // create plugin instance and save it in data
                item.data('UpdateList', new UpdateList(this, opt));
            } else {
                // if instance already created call method
                if(typeof opt === 'string') {
                    instance[opt](args);
                    console.log("Args: " + args);
                    console.log("opt: " + opt);
                }
            }
        });
    }

}(jQuery));
