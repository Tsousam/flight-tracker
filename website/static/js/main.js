var input = document.getElementById("departure");
new Awesomplete(input, {
	list: ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE", "Node.js", "Ruby on Rails"]
});


var input = document.getElementById("destination");
new Awesomplete(input, {
	list: ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE", "Node.js", "Ruby on Rails"]
});


// Flatpickr setup
flatpickr("#minMaxExample", {
  mode: "range",
  dateFormat: "d/m/Y",
  minDate: new Date(new Date().setDate(new Date().getDate() - 8)),
  maxDate: new Date(new Date().setDate(new Date().getDate() - 1)),
  locale: "en"
});
