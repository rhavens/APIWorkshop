(function(){
	// Keep this as a global variable for debugging purposes
	DataReceived = {"data":null};

	// Load our data!
	$(document).ready(function() {
		makeDataRequest();
	});

	function makeDataRequest() {
		console.log('Making request!');
		return $.ajax({
			url: '/api-test',
			contentType: 'text/plain',
			dataType: 'json',
			method: 'GET',
			success: function(data) { refreshSuccess(data); },
			error: function(a, b, c) { refreshError(a, b, c); }
		});
	}

	// handle data successfully loaded
	function refreshSuccess(data) {
		console.log(data);
		if ('data' in data) {
			// handle the new data
			DataReceived['data'] = data['data'];
			dataReceived();
		}
		else {
			// something went wrong
			refreshError('', '', '');
		}
	}

	// handle error and cry
	function refreshError(jqXHR, textStatus, errorThrown) {
		console.log('newDataReqFailure');
		console.log(jqXHR, textStatus, errorThrown);
		displayMessage('danger', 'Error', 'Something went wrong while fetching the data.');
	}

	///////////////
	// Essential UI updates
	///////////////

	function dataReceived(data) {
		displayMessage('success', 'Success', 'Successfully fetched data.');
		updateInterface();
	}

	function updateInterface() {
		console.log("Updating interface");
		// TODO - Make your data look nicer on the page!
		var location = DataReceived['data']['location']['city'];
		var temp_f = DataReceived['data']['current_observation']['temp_f'];
		$('#data').append($('<p>').text("Current temperature in " + location + " is " + temp_f + "°F."));
	}
	/***
	    General interface control
	                            ***/
	// Message display control
	// alert_type: success (green), info (blue), warning (yellow), danger (red)
	function displayMessage(alert_type,header,text) {
	    $('<div class="alert alert-'+alert_type+' alert-dismissible"><h4><strong>' +
	        header + ': </strong>' + text + 
	        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true"></span></button></h4></div>')
	        .hide().appendTo('.message').fadeIn(500).delay(3000).fadeOut(500)
	        .queue(function () { $(this).remove() });
	}

})(window);