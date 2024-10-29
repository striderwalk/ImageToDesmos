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
    if (event.target.files.length < 0) {
      return;
    }

    calculator.getExpressions().forEach(function (expression_state) {
      calculator.removeExpression(expression_state);
    });

    file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (event) {
      const data = JSON.parse(event.target.result);

      if (data.Polynomial) {
        // Add polynomials
        data.Polynomial.map((poly) => {
          calculator.setExpression({
            latex: poly,
            color: "#000000",
            folderId: "polynomial",
          });
        });
      }
      if (data.Line) {
        // Add Line
        data.Line.map((line) => {
          calculator.setExpression({
            latex: line,
            color: "#000000",
          });
        });
      }
      if (data.Circle) {
        // Add Circle
        data.Circle.map((circle) => {
          calculator.setExpression({
            latex: circle,
            color: "#000000",
          });
        });
      }

      if (data.Parametric) {
        // Add Parametric
        data.Parametric.map((parametric) => {
          calculator.setExpression({
            latex: parametric.equation,
            parametricDomain: {
              min: parametric.bounds.min,
              max: parametric.bounds.max,
            },
            color: "#000000",
          });
        });
      }
    };
    reader.readAsText(file);
  };
});
