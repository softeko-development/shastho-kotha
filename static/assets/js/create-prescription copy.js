const medicineSearchResultDiv = document.querySelector("#medicine_search_result");
const addedMedicine = document.querySelector("#added_medicines");

const getMedicineNameVal = () => {
  return document.getElementById("med_full_name").value;
};

// search result showing
function showSearchResult() {
  const medicineName = getMedicineNameVal();
  if (medicineName.length < 3) {
    return;
  }
  medicineSearchResultDiv.classList.add("active");
}

function hideSearchResult() {
  setTimeout(() => {
    medicineSearchResultDiv.classList.remove("active");
  }, 300);
}

let medicines = [];
function addMedicineHandler() {
  const medicineName = document.getElementById("med_full_name").value;
  const dosage = document.getElementById("medicine_dosage").value;
  const mealInstruction = document.getElementById("medicine_meal_instruction").value;
  const duration = document.getElementById("medicine_duration").value;
  const conditionalInstruction = document.getElementById("medicine_conditional_instruction").value;

  // Validate medicine name
  if (!medicineName) {
    const medicineNameError = document.querySelector(".medicine_name_error");
    if (medicineNameError) {
      medicineNameError.textContent = "Please select a medicine name";
    }
    return;
  } else {
    const medicineNameError = document.querySelector(".medicine_name_error");
    if (medicineNameError) {
      medicineNameError.textContent = "";
    }
  }

  if (!duration) {
    document.querySelector(".duration_error").textContent = "Please select a medicine taking duration";
    return;
  } else {
    document.querySelector(".duration_error").textContent = "";
  }

  if (dosage === "0") {
    document.querySelector(".dosage_error").textContent = "Please select a dosage";
    return;
  } else {
    document.querySelector(".dosage_error").textContent = "";
  }

  if (mealInstruction === "0") {
    document.querySelector(".meal_error").textContent = "Please select a Meal Instruction";
    return;
  } else {
    document.querySelector(".meal_error").textContent = "";
  }

  addedMedicine.innerHTML += `<tr>
                                <td>${medicineName}</td>
                                <td>${dosage}</td>
                                <td>${mealInstruction}</td>
                                <td>${conditionalInstruction}</td>
                                <td>${duration}</td>
                                <td class="text-end">
                                    <button class="btn btn-md rounded font-sm">Remove</button>
                                </td>
                            </tr>`;

  medicines.push({
    medicineName,
    dosage,
    mealInstruction,
    conditionalInstruction,
    duration,
  });

  removeMedicineHandler();
}

// remove medicine
function removeMedicineHandler() {
  const removeMedicineButtons = addedMedicine.querySelectorAll(".text-end");
  removeMedicineButtons.forEach((item) => {
    item.addEventListener("click", function (e) {
      this.parentElement.parentElement.remove();
    });
  });
}

// add medicine submit handler
const addMedicineFormBtn = document.querySelector("#add_medicine_form_submit_btn");

addMedicineFormBtn.addEventListener("click", function (e) {
  addMedicineHandler();
  return false;
});

// scrollbar
const medicineList = document.querySelector("#medicine_lists");
const ps = new PerfectScrollbar(medicineList);

function getIdsFromUrl() {
  const url = window.location.href;
  const regex = /\/create-prescription\/(\d+)\/(\d+)\/(\d+)\//;
  const matches = url.match(regex);

  if (matches) {
    return {
      doctorId: matches[1],
      patientId: matches[2],
      pharmacyId: matches[3],
    };
  } else {
    console.error('URL does not match the expected format');
    return null;
  }
}

function submitPrescription() {
  const ids = getIdsFromUrl();
  if (!ids) return;

  const medicines = Array.from(document.querySelectorAll('#added_medicines tr')).map(row => {
    const cells = row.querySelectorAll('td');
    return {
      medicineName: cells[0].textContent,
      dosage: cells[1].textContent,
      mealInstruction: cells[2].textContent,
      conditionalInstruction: cells[3].textContent,
      duration: cells[4].textContent,
    };
  });

  const selectedTests = document.getElementById('selected_tests').value;


  const prescriptionData = {
    doctor_id: ids.doctorId,
    patient_id: ids.patientId,
    pharmacy_id: ids.pharmacyId,
    problem: document.getElementById('problem').value,
    advice: document.getElementById('advice').value,
    notes: document.getElementById('additional_instruction').value,
    medicines: medicines,
    selected_tests: selectedTests
  };

  fetch(`/assign_prescription/`, {
    method: 'POST',
    body: JSON.stringify(prescriptionData),
    
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = '/prescription/patients_list/';
  } else {
      showErrorModal(data.error);
  }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred while creating the prescription.');
  });
}

document.querySelector('#submit_prescription_btn').addEventListener('click', function (e) {
  e.preventDefault(); // Prevent default form submission
  submitPrescription();
});


function showErrorModal(errorMessage) {
  const modalHtml = `
  <div class="modal fade" id="errorModal" tabindex="-1" aria-labelledby="errorModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="errorModalLabel">Error</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          ${errorMessage}
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);
  const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
  errorModal.show();
}

