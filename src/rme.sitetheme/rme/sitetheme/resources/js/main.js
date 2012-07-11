/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */

(function ($) {
    $(document).ready(function () {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
            // it's not realistic to think we can deal with all the bugs
            // of IE 6 and lower. Fortunately, all this is just progressive
            // enhancement.
            return;
        }
        $(function () {
            $('a[rel=tooltip]').tooltip();
        });
        $('a.popoverForm').prepOverlay({
            subtype: 'ajax',
            formselector: 'form',
            filter: '#content > *',
            noform: 'close',
            config: {
                expose: {color: '#fff'}
            }
        });
        $("#tooltip-expert, #tooltip-marketing, #tooltip-design, #tooltip-programming").tooltip({ effect: 'slide'});
        $(".chzn-select").chosen({
            no_results_text: "Keine Treffer gefunden"
        });
        $("#form-callback").validator();
        /* Apply to popup forms */
        $(document).bind('loadInsideOverlay', function (e) {
            $('select', $(this)).chosen({
                no_results_text: "Keine Treffer"
            });
            $('#form-callback', $(this)).validator();
        });
    });
}(jQuery));
