//GLOBALS
var hasSignedUp = false;

// Closes the sidebar menu
$("#menu-close").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
});

// Opens the sidebar menu
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("active");
});

// Scrolls to the selected menu item on the page
$(function() {
    $('a[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') || location.hostname == this.hostname) {

            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
		$('html,body').animate({
		    scrollTop: target.offset().top
		}, 1000);
		return false;
            }
        }
    });
});

// Opens the learn more boxes for each description
$(".learn-more").click(function(e) {
    var service_item = $( this ).parent()[0];
    var service_item_detail = $( $( this ).parents()[1] ).children()[1];
    $( service_item ).slideUp(function() {
	$( service_item_detail ).slideDown();	 
    });

});
$(".learn-less").click(function(e) {
    var service_item_detail = $( this ).parent()[0];
    var service_item = $( $( this ).parents()[1] ).children()[0];
    $( service_item_detail ).slideUp(function() {
	$( service_item ).slideDown();	 
    });
});

// Opens the signup/signin section above about and then travels to it
function scrollToElem(elem,delay){
    $('html, body').animate({
        scrollTop: $(elem).offset().top
    },delay);
}
// Set text field of signup area to show that user has already signed up
function setAlreadySignedUp(){
    $("#signup").show();
    $("#signup").find(".text-center").html(
	"<h2><font class=\"logo\" color=\"00B0DA\">Already Signed up!</font></h2>"
    );
    $( "#signup" ).delay( 2000 ).slideUp( 500 );
}

// Signup button handler
$(".signin").click(function(e) {
    if (hasSignedUp) { setAlreadySignedUp(); }
    hasSignedUp = true;
    $("#signup").show();
    scrollToElem("#signup",1000);
    $("#email").focus();       
});

// Hide signup area on enter
$("#signup-form").submit(function() {
    hasSignedUp = true;
    $("#signup").find(".input-group").hide();
    $("#signup").find(".fa-spin").show();             
    setTimeout(function () {
	var child_text = $("#signup").find(".text-center");
	child_text.delay( 2000 ).html(
	    "<h2><font class=\"logo\" color=\"00B0DA\">Thank You!</font><font class=\"logo\" color=\"ffb819\"></font></h2>"
	);
	setTimeout(function() {
	    $( "#signup" ).slideUp( 500 );
	}, 2000);	 
    }, 2000); 
    scrollToElem("#signup",1);
    return false;
});
