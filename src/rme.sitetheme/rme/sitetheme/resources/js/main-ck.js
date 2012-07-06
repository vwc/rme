/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true *//*global jQuery:false, document:false, window:false, location:false */(function(e) {
    e(document).ready(function() {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) return;
        e(function() {
            e("a[rel=tooltip]").tooltip();
        });
        e("a.popoverForm").prepOverlay({
            subtype: "ajax",
            formselector: "form",
            filter: "#content > *",
            noform: "close",
            config: {
                expose: {
                    color: "#fff"
                }
            }
        });
        e("#tooltip-marketing, #tooltip-design, #tooltip-programming").tooltip({
            effect: "slide"
        });
    });
})(jQuery);