    (function($){
        defaultOptions = {
            defaultId: 'selective_update_',
            listSelector: 'li'
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
            template: function(templateSkeleton) {
                this.templateSkeleton = templateSkeleton[0];
            },
            listener: function(newListener) {
                this.elementListener = newListener[0];
            },
            update: function(newArray) {
                idList = [];
                for(var i=0; i < newArray[0].length; i++){
                    idList.push(parseInt(newArray[0][i].id));
                }
                prefix = this.options.defaultId;
                $(this.options.listSelector).each(function(){
                    position = $.inArray(parseInt($(this).attr("id").replace(prefix, '')), idList)
                    if(position < 0){
                        $(this).slideUp('slow',function(){
                            $(this).off().remove();
                        });
                    } else {
                        idList.splice(position,1);
                        newArray[0].splice(position,1);
                    }
                });

                for(var i=0; i < newArray[0].length; i++){
                    newObject = buildTemplate(this.templateSkeleton, this.options.defaultId, newArray[0][i]);
                    $(newObject).appendTo($(this.item)).slideDown("slow");
                    (this.elementListener) ? this.elementListener(newObject) : console.log('no event listener set');
                }

                (this.options.onFinish) ? this.options.onFinish() : console.log('no onFinish callback');
            }
        }

        function buildTemplate(template, id_prefix, data){
            for(var key in data) {
                if (data.hasOwnProperty(key) && key != 'id') {
                    template = template.replace('{' + key + '}', data[key]);
                }
            }
            object = $.parseHTML(template);
            $(object).attr("id", id_prefix + String(data.id)).css("display", "none");
            return object;
        }

        // jQuery plugin interface
        $.fn.updateList = function(opt) {
            var args = Array.prototype.slice.call(arguments, 1);
            return this.each(function() {
                var item = $(this), instance = item.data('UpdateList');
                if(!instance) {
                    item.data('UpdateList', new UpdateList(this, opt));
                } else {
                    if(typeof opt === 'string') {
                        instance[opt](args);
                    }
                }
            });
        }
    }(jQuery));
