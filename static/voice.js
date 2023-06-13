function getCompletion() {
	$("#stream-text").html("Generating text...");
	let lang = $("#lang").val();
	let output = $("#output").val();
	let file = $("#file")[0].files[0];
	let mode = $('input[name="mode"]:checked').val();

var formData = new FormData();
    formData.append("file", file);
    formData.append("output", output);
    formData.append("lang", lang);
    formData.append("mode", mode);
    
    $.ajax({
        url: '/ASR',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            var assistantHTML = data;
            $("#stream-text").html(assistantHTML);
        },
        error: function() {
            console.log('Error generating text');
        }
    });
}
// allows message to be sent by clicking the Send button
$("#sendButton").click(function () {
	getCompletion();
});
