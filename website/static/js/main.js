var input = document.getElementById("departure");
new Awesomplete(input, {
	list: ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE", "Node.js", "Ruby on Rails"]
});


var input = document.getElementById("destination");
new Awesomplete(input, {
	list: ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE", "Node.js", "Ruby on Rails"]
});


// Flatpickr setup
flatpickr("#departureDate", {
  dateFormat: "d/m/Y",
  altFormat: "l, d/m/Y",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  autoClose: true,
  altInput: true
});

// Flatpickr setup
flatpickr("#dateRange", {
  mode: "range",
  dateFormat: "d/m/Y",
  altFormat: "l, d/m/Y",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  autoClose: true,
  altInput: true
});


// Toggle visibility based on checkbox
/* const checkbox = document.getElementById("isDateRange");
checkbox.addEventListener("change", function () {
  const single = document.getElementById("single-date-container");
  const range = document.getElementById("range-date-container");

  if (checkbox.checked) {
    single.style.display = "none";
    range.style.display = "block";
  } else {
    single.style.display = "block";
    range.style.display = "none";
  }
}); */


document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("isDateRange");
    const single = document.getElementById("single-date-container");
    const range = document.getElementById("range-date-container");

    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            single.classList.add("d-none");
            range.classList.remove("d-none");
        } else {
            single.classList.remove("d-none");
            range.classList.add("d-none");
        }
    });
});

