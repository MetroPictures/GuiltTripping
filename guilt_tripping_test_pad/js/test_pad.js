$(document).ready(function() {
	var hup = "hang_up";
	var pup = "pick_up";

	$("#mp_receiver")
		.html(pup)
		.click(function() {
			if($(this).html() == hup) {
				next_state = pup;
			} else if($(this).html() == pup) {
				next_state = hup;
			}

			$.ajax({
				url : $(this).html(),
				context : this
			}).done(function(json) {
				console.info(json);				
				$(this).html(next_state);
			});
		});
	
	var tr = $(document.createElement('tr'));
	for(var i=0; i<3; i++) {
		var html = "<p class=\"num\">" + i + "</p>";
		var td = $(document.createElement('td'));
		var a = $(document.createElement('a'))
			.html(html)
			.click(function() {
				var mapping = $($(this).find('.num')[0]).html();
				$.ajax({
					url : "mapping/" + mapping
				}).done(function(json) {
					console.info(json);
				});
			});

		$(td).append(a);
		$(tr).append(td);
	}

	$("#mp_main").append(tr);
});