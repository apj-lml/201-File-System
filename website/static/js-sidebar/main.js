(function($) {

	"use strict";

	var $sidebar = $('#sidebar');

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});
	};

	fullHeight();

	$('#sidebar').toggleClass('active');


	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

    // Detect clicks outside the sidebar and remove the 'active' class if it's active.
	$(document).click(function(event) {
		if (!$sidebar.is(event.target) && !$sidebar.has(event.target).length) {
			if (!$sidebar.hasClass('active')) {
				console.log('outside sidebar');
				// $sidebar.removeClass('active');
				$('#sidebar').toggleClass('active');
			}
		}else{
			console.log('inside sidebar');
		}
	  });
	

})(jQuery);
