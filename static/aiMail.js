var eventSource;

function getCompletion() {
  $("#stream-text").html("Generating Email...");
  let userText = $("#userMessage").val();
  let style = $('input[name="style"]:checked').val();

  if (eventSource) {
    eventSource.close(); // Close the existing connection if it exists
  }

  eventSource = new EventSource(
    "/emailRes?msg=" +
      encodeURIComponent(userText) +
      "&style=" +
      encodeURIComponent(style)
  );

  eventSource.onmessage = function (event) {
    var response = JSON.parse(event.data);
    var assistantHTML = response.content;
    console.log(assistantHTML);
    $("#stream-text").html(assistantHTML);

    // Check if the response indicates the end of streaming
    if (
      response.hasOwnProperty("streaming_completed") &&
      response.streaming_completed
    ) {
      eventSource.close(); // Close the connection
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
