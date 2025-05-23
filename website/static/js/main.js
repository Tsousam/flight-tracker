// Datepicker for Departure Date
flatpickr("#departure_date", {
  dateFormat: "d/m/Y",
  altFormat: "l, d/m/Y",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  autoClose: true,
  altInput: true
});

// Datepicker for Date Range
flatpickr("#departure_range", {
  mode: "range",
  dateFormat: "d/m/Y",
  altFormat: "l, d/m/Y",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  autoClose: true,
  altInput: true
});


document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("is_date_range");
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

// Code snippet adapted with the help of ChatGPT for Awesomplete setup and form validation.
// Ensures users can only submit the form after selecting valid values from the list.
const airportList = JSON.parse(document.getElementById("airport-list").textContent);

const departureInput = document.getElementById("departure");
const destinationInput = document.getElementById("destination");

new Awesomplete(departureInput, {
    list: airportList,
    minChars: 1,
    autoFirst: true
});

new Awesomplete(destinationInput, {
    list: airportList,
    minChars: 1,
    autoFirst: true
});

document.getElementById("search-form").addEventListener("submit", function (e) {
    const departure = departureInput.value.trim();
    const destination = destinationInput.value.trim();

    if (!airportList.includes(departure)) {
        e.preventDefault();
        alert("Please select a valid Airport for Departure.");
    }
    if (!airportList.includes(destination)) {
        e.preventDefault();
        alert("Please select a valid Airport for Destination.");
    }
});
