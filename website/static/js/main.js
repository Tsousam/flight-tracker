// Datepicker for Departure Date
flatpickr("#departure_date", {
  dateFormat: "Y/m/d",
  altFormat: "D d M",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  altInput: true
});

// Datepicker for Date Range
/* flatpickr("#departure_range", {
  mode: "range",
  dateFormat: "Y/m/d",
  altFormat: "D d M",
  minDate: new Date(), 
  maxDate: new Date(new Date().setFullYear(new Date().getFullYear() + 1)),
  locale: "en",
  altInput: true
}); */


document.addEventListener("DOMContentLoaded", () => {
    const checkbox = document.getElementById("is_date_range");
    const single = document.getElementById("single-date-container");
    const range = document.getElementById("range-date-container");

    range.classList.add("d-none");

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

// Code snippet adapted with the help of ChatGPT.
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("adults");
    const increaseButton = document.getElementById("increase-adults");
    const decreaseButton = document.getElementById("decrease-adults");

    increaseButton.addEventListener("click", function () {
      let currentValue = parseInt(input.value) || 0;
      if (currentValue < 9) {
        input.value = currentValue + 1;
      }
    });

    decreaseButton.addEventListener("click", function () {
      let currentValue = parseInt(input.value) || 0;
      if (currentValue > 0) {
        input.value = currentValue - 1;
      }
    });
  });

// Code snippet adapted with the help of ChatGPT for Awesomplete setup and form validation.
// Ensures users can only submit the form after selecting valid values from the list.
const airportList = JSON.parse(document.getElementById("airport-list").textContent);

const departureInput = document.getElementById("departure");
const destinationInput = document.getElementById("destination");
const departureDateInput = document.getElementById("departure_date")
const departureDateRangeInput = document.getElementById("departure-range")

function showError(msg) {
  const el = document.getElementById("date-error");
  el.classList.remove("d-none");
  el.textContent = msg;
}


document.getElementById("search-form").addEventListener("submit", function (e) {
    const departure = departureInput.value.trim();
    const destination = destinationInput.value.trim();
    const departureDate = departureDateInput.value.trim();
    const departureDateRange = flatpickrInstance.parseDate(departureDate, "d/m/Y");
    const today = new Date();
    const maxDate = new Date();
    const range = departureDateRange.value.split(" to ");
    

    if (!airportList.includes(departure)) {
        e.preventDefault();
        alert("Please select a valid Airport for Departure.");
    }
    if (!airportList.includes(destination)) {
        e.preventDefault();
        showError("Please select a valid Airport for Destination.");
    }
    if (departure === destination) {
        alert("Departure and Destination cannot be the same.");
        return false;
    }
    if (!departureDate) {
        showError("Please select a date.");
        return false;
    }
    if (departureDateRange < today) {
        showError("Selected date cannot be in the past.");
        return false;
    }
    maxDate.setFullYear(maxDate.getFullYear() + 1);
    if (departureDateRange > maxDate) {
        showError("Selected date must be within 1 year.");
        return false;
    }
    if (range.length !== 2) {
        showError("Please select both a start and an end date.");
        return false;
    }
});


const awesompleteDeparture = new Awesomplete(departureInput, {
    list: airportList,
    maxItems: 5,
    minChars: 1,
    autoFirst: true
});

const awesompleteDestination = new Awesomplete(destinationInput, {
    list: airportList,
    maxItems: 5,
    minChars: 1,
    autoFirst: true
});


departureInput.addEventListener("focus", function () {
    awesompleteDeparture.evaluate();
});

destinationInput.addEventListener("focus", function () {
    awesompleteDestination.evaluate();
});


function closeDropdownOnSelect() {
    this.blur();
}

departureInput.addEventListener("awesomplete-selectcomplete", closeDropdownOnSelect);
destinationInput.addEventListener("awesomplete-selectcomplete", closeDropdownOnSelect);