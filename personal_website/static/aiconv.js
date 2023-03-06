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
	$.get("/AiResponse", { msg: userText }).done(function (data) {
		var assistantHTML =
			'<div class="media media-chat"><div class="media-body">' +
			data +
			"</div></div>";
		$("#messagebox").append(assistantHTML);
		document
			.getElementById("zzz")
			.scrollIntoView({ block: "start", behavior: "smooth" });
	});
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
