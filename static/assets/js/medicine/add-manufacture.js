const brandName = document.querySelector("#brand_name");
const brandLogo = document.querySelector("#brand_logo");
const liveToast = document.querySelector("#liveManufactureToast");
const toastBody = document.querySelector(".toast-body");
const brandContainer = document.querySelector("#brand_container");
const logoPreview = document.querySelector("#logoPreview");
const rootUrl = "http://127.0.0.1:8000";
let brandFormType = "add";
let editBrandId;

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

// brand submit handler
function brandSubmitHandler() {
  if (brandFormType === "add") {
    addNewBrandHandler();
  } else {
    editBrandHandler();
  }
}

// add brand function
async function addNewBrandHandler() {
  if(!brandName.value){
    document.querySelector(".brand_name_error").textContent = "please enter a name";
    return;
  }
  formdata.append("name", brandName.value);
  formdata.append("logo", brandLogo.files[0]);

  $.ajax({
    url: "/api/companies/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
      brandName.value = "";
      document.querySelector(".brand_name_error").textContent = "";
      toastBody.textContent = "Brand created successfully";

      liveToast.classList.add("show");
      getAllBrands();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveToast.classList.add("show");
    },
  });
}

// get all brands function
async function getAllBrands() {
  $.ajax({
    url: "/api/companies/",
    type: "GET",
    success: function (response) {
      brandContainer.innerHTML = "";

      response.map((item) => {
        const logo = item.logo ? item.logo : "plogo/placeholder.png";
        brandContainer.innerHTML += `<div class="col-xl-2 col-lg-3 col-md-4 col-6">
                    <figure class="card border-1">
                        <div class="card-header dropdown bg-white text-center">
                            <img height="76" src="${rootUrl}/media/${logo}" alt="Logo" />
                            <a class="dropdown-toggle edit_icon user_edit_icon" data-bs-toggle="dropdown" href="#"
                                aria-expanded="false">
                                <i class="icon material-icons md-more_horiz"></i>
                            </a>
                            <div class="edit_overlay dropdown-menu">
                                <ul class="list-unstyled">
                                    <a data-bs-toggle="modal" data-bs-target="#viewBrandModal" onclick="showEditModal(${item.id})" class="dropdown-item">Edit</a>
                                    <a onclick="brandDeleteHandler(${item.id})" class="dropdown-item">Delete</a>
                                </ul>
                            </div>
                        </div>
                        <figcaption class="card-body text-center">
                            <h6 class="card-title m-0">${item.name}</h6>
                        </figcaption>
                    </figure>
                </div>`;
      });
    },
    error: function (response) {
      console.error(response.errors);
    },
  });
}
getAllBrands();

// function show edit modal
function showEditModal(id) {
  brandFormType = "edit";
  editBrandId = id;
  $.ajax({
    url: `/api/companies/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        brandName.value = response.name || "";

        if (response.logo) {
          if (logoPreview) {
            logoPreview.src = `${rootUrl}${response.logo}`;
            logoPreview.style.display = "block";
          }
        }
      } else {
        console.error("Failed to load brand data.");
      }
    },
    error: function (response) {
      console.error("Failed to load brand data:", response);
    },
  });
}

// function show edit modal
function hideEditModal() {
  brandFormType = "add";
  editBrandId = "";
  brandName.value = "";
}

// editbrandhandler
async function editBrandHandler() {
  if(!brandName.value){
    document.querySelector(".brand_name_error").textContent = "please enter a name";
    return;
  }
  if (brandName.value) {
    formdata.set("name", brandName.value);
  }
  if (brandName?.files?.length !== 0) {
    formdata.set("logo", brandLogo.files[0]);
  }

  $.ajax({
    url: `/api/companies/${editBrandId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllBrands();
        brandFormType = "add";
        editBrandId = "";
        brandName.value = "";
        document.querySelector(".brand_name_error").textContent = "";
        toastBody.textContent = "Brand updated successfully";
        liveToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveToast.classList.add("show");
      }
    },
  });
}

// deletebrandhandler
async function brandDeleteHandler(companyId) {
  $.ajax({
    url: `/api/companies/${companyId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllBrands();
        toastBody.textContent = "Brand deleted successfully";
        liveToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveToast.classList.add("show");
      }
    },
  });
}
