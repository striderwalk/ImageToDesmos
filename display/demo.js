var elt = document.getElementById("calculator");
var calculator = Desmos.GraphingCalculator(elt);

var pixelCoordinates = calculator.graphpaperBounds.pixelCoordinates;
var mathCoordinates = calculator.graphpaperBounds.mathCoordinates;

var asp = mathCoordinates.height / mathCoordinates.width;

calculator.setMathBounds({
  left: 0,
  right: 400,
  bottom: 0,
  top: asp * 400,
});
function display_curves(data) {
  data.forEach((element) => {
    // console.log(element);
    calculator.setExpression({
      latex: element,
      color: "#000000",
    });
  });
}
fetch("../functions.txt")
  .then((response) => response.text())
  .then((data) => {
    display_curves(data.split("\n"));
  })
  .catch((error) => console.error("Error loading file:", error));
