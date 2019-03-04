// Copyright (c) 2011 Clarified Networks
// AHEvent is a constructor for an AbuseHelper-style event object.
//
// Previously each AHEvent instance stored key-valuelist pairs in an
// object, e.g.:
//
//   attrs = {
//     key1: [value1A],
//     key2: [value2A, value2B],
//     ...
//   };
//
// This seems to consume a lot of memory on the current browser
// JavaScript engines, especially on Nitro/Safari and V8/Chrome. To
// save memory, the current AHEvent implementation stores the
// key-value data in an array, e.g.:
//
//   attrs = [key1, value1A, key2, value2A, key2, value2B, ...];
//
// The array is semi-lazily sorted by the keys (when the sorted order
// is actually needed for the first time). Values for a given key can
// then be found by doing a binary search over the keys.

(function(exports) {
    var hasOwnProperty = Object.prototype.hasOwnProperty;
    var toString = Object.prototype.toString;

    var isArray = Array.isArray || function(obj) {
        return toString.call(obj) === "[object Array]";
    };
    
    var forceArray = function(values) {
        return isArray(values) ? values : [values];
    };

    var sortCmp = function(left, right) {
        // Test only the less-than case. Order doesn't matter
        // if the keys are equal.
        return right.key < left.key ? 1 : -1;
    };

    var sort = function(attrs) {
        var keys = [];
        for (var i = 0, len = attrs.length; i < len; i += 2) {
            keys.push({
                "key": attrs[i],
                "value": attrs[i+1]
            });
        }
        keys.sort(sortCmp);
        
        for (var i = 0, len = keys.length; i < len; i++) {
            var item = keys[i];
            attrs[(i << 1)] = item.key;
            attrs[(i << 1) + 1] = item.value;
        }
    };
    
    var find = function(attrs, key) {
        var lo = 0;
        var hi = attrs.length >> 1;
        
        while (lo < hi) {
            var mid = lo + ((hi - lo) >> 1);
            var item = attrs[mid << 1];
            
            if (item < key) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }

        return lo << 1;
    };

    var DEFAULT_MAP = function(value) {
        return value;
    };

    var DEFAULT_FILTER = function(value) {
        return (value != null) && (!isNaN(value));
    };

    var fillMapFilter = function(mapFilter) {
        if (typeof(mapFilter) === "function") {
            return {
                "map": mapFilter,
                "filter": DEFAULT_FILTER
            };
        } 

        return {
            "map": mapFilter.map || DEFAULT_MAP,
            "filter": mapFilter.filter || DEFAULT_FILTER
        };
    };

    var AHEvent = exports.AHEvent = function(object) {
        var attrs = null;
        var sorted = false;

        if (object instanceof AHEvent) {
            attrs = object.attrs.slice(0, object.attrs.length);
            sorted = object.sorted;
        } else if (isArray(object)) {
            attrs = object.slice(0, (object.length >> 1) << 1);
        } else if (object) {
            attrs = [];
            for (var key in object) {
                if (!hasOwnProperty.call(object, key)) continue;
                
                var values = forceArray(object[key]);
                for (var i = 0, len = values.length; i < len; i++) {
                    attrs.push(key);
                    attrs.push(values[i]);
                }
            }
        }
        
        this.attrs = attrs || [];
        this.sorted = sorted;
    };
    
    AHEvent.NS = "abusehelper#event";
    
    AHEvent.prototype = {
        sorted: false,
        attrs: null,

        _sortedAttrs: function() {
            var attrs = this.attrs;
            if (!this.sorted) {
                sort(attrs);
                this.sorted = true;
            }
            return attrs;
        },

        values: function(key, mapFilter, context) {
            var attrs = this._sortedAttrs();
            var start = find(attrs, key);
            var end = attrs.length;
            
            var values = [];            

            if (!mapFilter) {
                for (var i = start; i < end && attrs[i] === key; i += 2) {
                    values.push(attrs[i+1]);
                }
            } else {
                mapFilter = fillMapFilter(mapFilter);
                var map = mapFilter.map;
                var filter = mapFilter.filter;
                
                for (var i = start; i < end && attrs[i] === key; i += 2) {
                    var value = map.call(context, attrs[i+1]);
                    if (filter.call(context, value)) values.push(value);
                }                
            }
            
            return values;
        },

        items: function(){
            var items = {};
            var attrs = this._sortedAttrs();
            for (var i = 0, eLength = attrs.length; i < eLength; i++) {
                //var item = attrs[i];
                if(i % 2 === 0){
                    //var values = [];
                    items[attrs[i]] = this.values(attrs[i]);
                }
            }
            return items;
        },

        value: function(key, defaultValue, mapFilter, context) {
            var attrs = this._sortedAttrs();
            var start = find(attrs, key);
            var end = attrs.length;
            
            if (!mapFilter) {
                if (start < end && attrs[start] === key) {
                    return attrs[start+1];
                }
            } else {
                mapFilter = fillMapFilter(mapFilter);
                var map = mapFilter.map;
                var filter = mapFilter.filter;
                
                for (var i = start; i < end && attrs[i] === key; i += 2) {
                    var value = map.call(context, attrs[i+1]);
                    if (filter.call(context, value)) return value;
                }                
            }

            if (arguments.length >= 2) {
                return defaultValue;
            } else {
                return null;
            }
        },
    
        isValid: function() {
            var attrs = this.attrs;
            for (var i = 0, len = attrs.length; i < len; i += 2) {
                if (attrs[i] !== "id") return true;
            }
            return false;
        },
    
        forEach: function(func, context) {
            var attrs = this.attrs;
            for (var i = 0, len = attrs.length; i < len; i += 2) {
                func.call(context, attrs[i+1], attrs[i], this);
            }
        },
        
        toElement: function() {
            var event = new Element("event", { xmlns: AHEvent.NS });
            
            this.forEach(function(value, key) {
                var attr = new Element("attr");
                attr.setAttribute("key", key);
                attr.setAttribute("value", value);
                event.grab(attr);
            });
            
            return event;
        }
    };

    AHEvent.fromElements = function(elements) {
        var events = [];
        
        for (var i = 0, eLength = elements.length; i < eLength; i++) {
            var element = elements[i];
            if (!element.tagName) continue;
            if (element.tagName.toLowerCase() !== "event") continue;
	    if (element.getAttribute("xmlns") !== AHEvent.NS) continue;
            
            var attrs = {};
	    var children = element.childNodes;
	    for (var j = 0, cLength = children.length; j < cLength; j++) {
                var child = children[j];
                if (!child.tagName) continue;
                if (child.tagName.toLowerCase() !== "attr") continue;
                
                var key = child.getAttribute("key");
                var value = child.getAttribute("value");
                
                if (key !== null && value !== null) {
                    attrs[key] = attrs[key] || [];
		            attrs[key].push(value);
                }
            }
            events.push(new AHEvent(attrs));
        }
        
        return events;       
    };
})(this);
