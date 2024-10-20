let calculator;

// Wait until the DOM is fully loaded before attaching event listeners
document.addEventListener("DOMContentLoaded", function () {
  var calculator_element = document.getElementById("calculator");
  calculator = Desmos.GraphingCalculator(calculator_element);

  var mathCoordinates = calculator.graphpaperBounds.mathCoordinates;

  var asp = mathCoordinates.height / mathCoordinates.width;

  calculator.setMathBounds({
    left: 0,
    right: 400,
    bottom: 0,
    top: asp * 400,
  });

  // When the user clicks the button, trigger the file input
  document
    .getElementById("selectFileButton")
    .addEventListener("click", function () {
      document.getElementById("fileInput").click();
    });

  // When a file is selected
  document.getElementById("fileInput").onchange = function (event) {
    if (event.target.files.length > 0) {
      calculator.getExpressions().forEach(function (expression_state) {
        calculator.removeExpression(expression_state);
      });
      // Get the selected file
      const file = event.target.files[0];

      // Create a new FileReader object
      const reader = new FileReader();

      // Define what happens when the file is read
      reader.onload = function (e) {
        // Get the file content (e.target.result contains the file data)
        const fileContent = e.target.result;

        // Split content by new lines to get an array of lines
        const lines = fileContent.split(/\r?\n/); // This handles both Windows (\r\n) and Unix (\n) line endings

        // Apply a function to each line
        lines.forEach((element, index) => {
          console.log(element);
          calculator.setExpression({
            latex: element,
            color: "#000000",
          });
        });
      };

      // Read the file as text
      reader.readAsText(file);
    } else {
      // No file selected, prompt again
      alert("Please select a file to proceed.");
    }
  };
});
