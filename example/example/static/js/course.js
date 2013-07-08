/**
 * Course namespace.
 */
var course = (function(global, $) {
    var CourseController = klass(function(params) {
        // initilize params.
        this._courseStreamURL = params.courseStreamURL;
        this._courseStateURL = params.courseStateURL;
        this._courseStartURL = params.courseStartURL;
        this._courseStopURL = params.courseStopURL;

        // set everything up.
        this._setupSSE();
        this._setupUIListeners();

        // show the current state.
        this._loadCurrentCourseState();
    }).methods({
        /**
         * Setup the event stream for course state.
         * If EventSource unavailable, fallback to xHR pooling.
         */
        _setupSSE: function() {
            // check if this browser has SSE capability.
            if (global.EventSource) {
                var eventSource = new EventSource(this._courseStreamURL);

                eventSource.addEventListener("state", function(e) {
                    $("#current-course-state").html(e.data);
                });
            }
            else {
                this._setupSSEFallback();
            }
        },

        /**
         * Setup a simple fallback for the SSE capability using a xHR pooling.
         */
        _setupSSEFallback: function() {
            setTimeout(_loadCurrentCourseState, 2000);
        },

        /**
         * Setup UI listeners of the course state test page.
         */
        _setupUIListeners: function() {
            var _self = this;

            $("#start-button").on("click", function() {
                $.ajax({url: _self._courseStartURL});
            });
            $("#stop-button").on("click", function() {
                $.ajax({url: _self._courseStopURL});
            });
        },

        /**
         * Load the current course state by performing an ajax call.
         */
        _loadCurrentCourseState: function() {
            $("#current-course-state").load(this._courseStateURL);
        }
    });

    return {
        CourseController: CourseController
    };
})(window, jQuery);