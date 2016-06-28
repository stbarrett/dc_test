$(document).ready(function() {	
	/* Main Nav */
	$("ul#nav li").not("ul#nav li ul li").hover(
	  function () {
		$("a", this).addClass("hover");
		$(this).find(".dropdown").show(0);
	  },
	  function () {
		$("a", this).removeClass("hover");
		$(this).find(".dropdown").hide(0);
	  }
	);

	$('#searchBtn').click(function() {
		  $('#searchform').submit();
		  return false;
	});
	
	// setup add links
	$(".add-mystuff a").click(function() {
		$(".add-mystuff .adding").slideDown(50);
		$.post("/mystuff/collectibles/add/", { item_id: item_id },
			function(data){
			$(".add-mystuff .adding").slideUp(50);
			if(data == 0) {	// not logged in
				showSignInDialog();
			} else if(data == 1) { // done
				$(".add-mystuff").empty().html('<div class="ihave"><div class="ui-button ui-widget ui-state-disabled ui-corner-all ui-button-text-only ui-state-focus"><span class="ui-button-text">I have this</span></div></div>');
				$("#added-msg").slideDown(300);
			} else if(data == 2) {	// already have
				$(".add-mystuff").empty().html('<div class="ihave"><div class="ui-button ui-widget ui-state-disabled ui-corner-all ui-button-text-only ui-state-focus"><span class="ui-button-text">I have this</span></div></div>');
			}
		});
		
		return false;

	});
	
	$(".add-wishlist a").click(function() {
		$(".add-wishlist .adding").slideDown(50);
		$.post("/mystuff/wishlist/add/", { item_id: item_id },
			function(data){
			$(".add-wishlist .adding").slideUp(50);
			if(data == 0) {	// not logged in
				showSignInDialog();
			} else if(data == 1) { // done
				$(".add-wishlist").empty().html('<div class="ihave" style="margin-left:10px;"><div class="ui-button ui-widget ui-state-disabled ui-corner-all ui-button-text-only ui-state-focus"><span class="ui-button-text">In my wish list</span></div></div>');
				$("#added-msg").slideDown(300);
			} else if(data == 2) {	// already have
				$(".add-wishlist").empty().html('<div class="ihave" style="margin-left:10px;"><div class="ui-button ui-widget ui-state-disabled ui-corner-all ui-button-text-only ui-state-focus"><span class="ui-button-text">In my wish list</span></div></div>');
			}
		});
		
		return false;
	});	

	
	// setup contribute links
	$("#submit-image").click(function() {
		$.get('/member/user-signed-in/', function(data) {
			if(Boolean(data)){
				$.fn.colorbox({href:$("#submit-image").attr('href'), width:"90%",height:"90%",iframe:true,scrolling:true,overlayClose:false})
			} else {
				showSignInDialog();
			}
		});
		return false;
	});
});

// submit form, grab show items
function submitSearchForm() {
	v = "";
	page = $("#page").val();
	query = $("#query").val();
	t = $("#t").val();
	url = "/search/";
	checkboxes = Array('sortPins', 'sortDollars');
	$('#sort-container input:checkbox').each( function() {
		if(this.checked) {
			v += $(this).val() + "|";
		}
	});
	val = v.substring(0, v.length - 1);
	url += "?query="+query;
	if(t) { url += "&t=" + t; }
	if(val) { url += "&show=" + val; }
	
	window.location = url;
	
	return false;
}

function showSignInDialog() {
	$('#signin-required-dialog').dialog('open');
}

