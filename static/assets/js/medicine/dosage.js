const dosageName = document.querySelector("#dosage_name");
const liveDosageToast = document.querySelector("#liveDosageToast");
const toastBody = document.querySelector("#liveDosageToast .toast-body");
const dosageContainer = document.querySelector("#dosage_container");
const rootUrl = "http://127.0.0.1:8000";
let dosageFormType = "add";
let editdosageId;

// gettting csrf token
function getCSRFToken() {
  let cookieValue = null;
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      cookieValue = decodeURIComponent(cookie.substring("csrftoken=".length));
      break;
    }
  }
  return cookieValue;
}
const csrftoken = getCSRFToken();

const formdata = new FormData();

// dosage submit handler
function dosageSubmitHandler() {
  if (dosageFormType === "add") {
    addNewdosageHandler();
  } else {
    editdosageHandler();
  }
}

// add dosage function
async function addNewdosageHandler() {
  if(!dosageName.value){
    document.querySelector(".dosage_name_error").textContent = "please enter a name";
    return;
  }
  formdata.append("name", dosageName.value);

  $.ajax({
    url: "/api/dosages/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
        dosageName.value = ""
        document.querySelector(".dosage_name_error").textContent = "";
      toastBody.textContent = "dosage created successfully";

      liveDosageToast.classList.add("show");
      getAllDosages();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveDosageToast.classList.add("show");
    },
  });
}

// get all Dosages function
async function getAllDosages() {
  $.ajax({
    url: "/api/dosages/",
    type: "GET",
    success: function (response) {
      dosageContainer.innerHTML = "";

      response.map((item) => {
        dosageContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.name}</h6>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewDosageModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="dosageDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
                                class="material-icons md-delete_forever"></i> Delete </a>
                    </div>
                </div>
            </article>`;
      });
    },
    error: function (response) {
      console.error(response.errors);
    },
  });
}
getAllDosages();

// function show edit modal
function showEditModal(id) {
  dosageFormType = "edit";
  editdosageId = id;
  $.ajax({
    url: `/api/dosages/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        dosageName.value = response.name || "";
      } else {
        console.error("Failed to load dosage data.");
      }
    },
    error: function (response) {
      console.error("Failed to load dosage data:", response);
    },
  });
}


// function show edit modal
function hideEditModal() {
    dosageFormType = "add";
    editdosageId = "";
    dosageName.value = ""
}



// editdosagehandler
async function editdosageHandler() {
  if(!dosageName.value){
    document.querySelector(".dosage_name_error").textContent = "please enter a name";
    return;
  }
  if (dosageName.value) {
    formdata.set("name", dosageName.value);
  }

  if(!editdosageId){
    return;
  }

  $.ajax({
    url: `/api/dosages/${editdosageId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllDosages();
        editdosageId = "";
        dosageFormType = "add";
        dosageName.value = "";
        document.querySelector(".dosage_name_error").textContent = "";
        toastBody.textContent = "dosage updated successfully";
        liveDosageToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveDosageToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveDosageToast.classList.add("show");
      }
    },
  });
}

// deletedosagehandler
async function dosageDeleteHandler(dosageId) {
  $.ajax({
    url: `/api/dosages/${dosageId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllDosages();      
        toastBody.textContent = "dosage deleted successfully";
        liveDosageToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveDosageToast.classList.add("show");
      }
    },
  });
}
