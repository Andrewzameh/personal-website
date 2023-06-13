var eventSource;
var currentBubbleId = 0; // Track the ID of the current chat bubble

function createChatBubble() {
    currentBubbleId++; // Increment the bubble ID
    var bubbleHtml =
        '<div id="bubble-' + currentBubbleId + '" class="media media-chat"><div class="media-body"></div></div>';
    $("#messagebox").append(bubbleHtml);
    return "#bubble-" + currentBubbleId;
}

function getCompletion() {
	let userText = $("#userMessage").val();
	let userHtml =
		'<div class="d-flex media media-chat media-chat-reverse"><div class="media-body"><p>' +
		userText +
		"</p></div></div>";
	$("#userMessage").val("");
	$("#messagebox").append(userHtml);
	document
		.getElementById("zzz")
		.scrollIntoView({ block: "start", behavior: "smooth" });
	
	if (eventSource) {
		eventSource.close(); // Close the existing connection if it exists
	}

	var currentBubble = createChatBubble();

	eventSource = new EventSource(
        "/AiResponse?msg=" +
        encodeURIComponent(userText));

	eventSource.onmessage = function (event) {
		var response = JSON.parse(event.data);
		$(currentBubble + " .media-body").html(response.content);
		document
			.getElementById("zzz")
			.scrollIntoView({ block: "start", behavior: "smooth" });

			
		if (
			response.hasOwnProperty("streaming_completed") &&
			response.streaming_completed
			) {
				eventSource.close(); // Close the connection
				currentBubbleId++;
		}
	};
}


$("#userMessage").keypress(function (e) {
	// allows message to be sent with enter key
	if (e.which == 13) {
		getCompletion();
	}
});
// allows message to be sent by clicking the Send button
$("#sendButton").click(function () {
	getCompletion();
});
