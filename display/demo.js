var elt = document.getElementById("calculator");
var calculator = Desmos.GraphingCalculator(elt);
calculator.resize();
function display_curves(data) {
  data.forEach((element) => {
    console.log(element);
    calculator.setExpression({
      latex: element,
      color: "#000000",
    });
  });
}
fetch("../functions.txt") // Fetch a JSON file from the same directory as the HTML
  .then((response) => response.text())
  .then((data) => {
    display_curves(data.split("\n")); // Do something with the data
  })
  .catch((error) => console.error("Error loading file:", error));
