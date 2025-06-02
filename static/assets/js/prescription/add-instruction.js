const instructionName = document.querySelector("#instruction_name");
const liveInstructionToast = document.querySelector("#liveInstructionToast");
const toastBody = document.querySelector("#liveInstructionToast .toast-body");
const instructionContainer = document.querySelector("#instruction_container");
const rootUrl = "http://127.0.0.1:8000";
let instructionFormType = "add";
let editinstructionId;

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

// instruction submit handler
function instructionSubmitHandler() {
  if (instructionFormType === "add") {
    addNewinstructionHandler();
  } else {
    editinstructionHandler();
  }
}

// add instruction function
async function addNewinstructionHandler() {
  if(!instructionName.value){
    document.querySelector(".instruction_name_error").textContent = "please enter a name";
    return;
  }
  formdata.append("instruction", instructionName.value);

  $.ajax({
    url: "/api/instructions/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
        instructionName.value = ""
        document.querySelector(".instruction_name_error").textContent = "";
      toastBody.textContent = "instruction created successfully";

      liveInstructionToast.classList.add("show");
      getAllInstructions();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveInstructionToast.classList.add("show");
    },
  });
}

// get all Instructions function
async function getAllInstructions() {
  $.ajax({
    url: "/api/instructions/",
    type: "GET",
    success: function (response) {
      instructionContainer.innerHTML = "";

      response.map((item) => {
        instructionContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.instruction}</h6>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewInstructionModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="instructionDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
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
getAllInstructions();

// function show edit modal
function showEditModal(id) {
  instructionFormType = "edit";
  editinstructionId = id;
  $.ajax({
    url: `/api/instructions/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        instructionName.value = response.instruction || "";
      } else {
        console.error("Failed to load instruction data.");
      }
    },
    error: function (response) {
      console.error("Failed to load instruction data:", response);
    },
  });
}


// function show edit modal
function hideEditModal() {
    instructionFormType = "add";
    editinstructionId = "";
    instructionName.value = ""
}



// editinstructionhandler
async function editinstructionHandler() {
  if(!instructionName.value){
    document.querySelector(".instruction_name_error").textContent = "please enter a name";
    return;
  }
  if (instructionName.value) {
    formdata.set("instruction", instructionName.value);
  }

  if(!editinstructionId){
    return;
  }

  $.ajax({
    url: `/api/instructions/${editinstructionId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllInstructions();
        editinstructionId = "";
        instructionFormType = "add";
        instructionName.value = "";
        document.querySelector(".instruction_name_error").textContent = "";
        toastBody.textContent = "instruction updated successfully";
        liveInstructionToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveInstructionToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveInstructionToast.classList.add("show");
      }
    },
  });
}

// deleteinstructionhandler
async function instructionDeleteHandler(companyId) {
  $.ajax({
    url: `/api/instructions/${companyId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllInstructions();      
        toastBody.textContent = "instruction deleted successfully";
        liveInstructionToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveInstructionToast.classList.add("show");
      }
    },
  });
}
