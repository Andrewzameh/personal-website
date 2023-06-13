var eventSource;

function getCompletion() {
  $("#stream-text").html("Generating Answer...");
  let question = $("#question").val();
  console.log("question: " + question);
  let mode = $('input[name="mode"]:checked').val();
  console.log("mode: " + mode);
  $("#submit").prop("disabled", true);
  
  
  if (eventSource) {
    eventSource.close(); // Close the existing connection if it exists
  }
  
  eventSource = new EventSource(
    "/QARes?question=" +
    encodeURIComponent(question) +
    "&mode=" +
    encodeURIComponent(mode)
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
      $("#submit").prop("disabled", false);
    }
  };
}
$("#question").keypress(function (e) {
  // allows message to be sent with enter key
  if (e.which == 13) {
    getCompletion();
  }
});
// allows message to be sent by clicking the Send button
$("#submit").click(function () {
  getCompletion();
});
