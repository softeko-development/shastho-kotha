const genericName = document.querySelector("#generic_name");
const liveGenericToast = document.querySelector("#liveGenericToast");
const toastBody = document.querySelector("#liveGenericToast .toast-body");
const genericContainer = document.querySelector("#generic_container");
const rootUrl = "http://127.0.0.1:8000";
let genericFormType = "add";
let editgenericId;

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

// generic submit handler
function genericSubmitHandler() {
  if (genericFormType === "add") {
    addNewgenericHandler();
  } else {
    editgenericHandler();
  }
}

// add generic function
async function addNewgenericHandler() {
  if (!genericName.value) {
    document.querySelector(".generic_name_error").textContent =
      "please enter a name";
    return;
  }
  formdata.append("name", genericName.value);

  $.ajax({
    url: "/api/generics/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
      genericName.value = "";
      document.querySelector(".generic_name_error").textContent = "";
      toastBody.textContent = "generic created successfully";

      liveGenericToast.classList.add("show");
      getAllGenerics();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveGenericToast.classList.add("show");
    },
  });
}

// get all generics function
async function getAllGenerics() {
  $.ajax({
    url: "/api/generics/",
    type: "GET",
    success: function (response) {
      genericContainer.innerHTML = "";

      response.map((item) => {
        genericContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.name}</h6>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewGenericModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="genericDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
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
getAllGenerics();

// function show edit modal
function showEditModal(id) {
  genericFormType = "edit";
  editgenericId = id;
  $.ajax({
    url: `/api/generics/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        genericName.value = response.name || "";
      } else {
        console.error("Failed to load generic data.");
      }
    },
    error: function (response) {
      console.error("Failed to load generic data:", response);
    },
  });
}

// function show edit modal
function hideEditModal() {
  genericFormType = "add";
  editgenericId = "";
  genericName.value = "";
}

// editgenerichandler
async function editgenericHandler() {
  if (!genericName.value) {
    document.querySelector(".generic_name_error").textContent =
      "please enter a name";
    return;
  }
  if (genericName.value) {
    formdata.set("name", genericName.value);
  }

  if (!editgenericId) {
    return;
  }

  $.ajax({
    url: `/api/generics/${editgenericId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllGenerics();
        editgenericId = "";
        genericFormType = "add";
        genericName.value = "";
        document.querySelector(".generic_name_error").textContent = "";
        toastBody.textContent = "generic updated successfully";
        liveGenericToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveGenericToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveGenericToast.classList.add("show");
      }
    },
  });
}

// deletegenerichandler
async function genericDeleteHandler(genericId) {
  $.ajax({
    url: `/api/generics/${genericId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllGenerics();
        toastBody.textContent = "generic deleted successfully";
        liveGenericToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveGenericToast.classList.add("show");
      }
    },
  });
}
