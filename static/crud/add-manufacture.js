const brandName = document.querySelector("#brand_name");
const brandLogo = document.querySelector("#brand_logo");
const liveToast = document.querySelector("#liveManufactureToast");
const toastBody = document.querySelector(".toast-body");
const brandContainer = document.querySelector("#brand_container");
const rootUrl = "http://127.0.0.1:8000/";
let brandFormType = "add";
let editBrandId;

// Getting CSRF token
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

// Brand submit handler
function brandSubmitHandler() {
  if (brandFormType === "add") {
    addNewBrandHandler();
  } else {
    editBrandHandler();
  }
}

// Add brand function
async function addNewBrandHandler() {
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

// Get all brands function
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
                            <img height="76" src="${rootUrl}media/${logo}" alt="Logo" />
                            <a class="dropdown-toggle edit_icon user_edit_icon" data-bs-toggle="dropdown" href="#"
                                aria-expanded="false">
                                <i class="icon material-icons md-more_horiz"></i>
                            </a>
                            <div class="edit_overlay dropdown-menu">
                                <ul class="list-unstyled">
                                    <a data-bs-toggle="modal" data-bs-target="#EditBrandModal" onclick="showEditModal(${item.id})" class="dropdown-item">Edit</a>
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

function showEditModal(id) {
  brandFormType = "edit";
  editBrandId = id;

  $.ajax({
      url: `/api/companies/${id}/`,
      type: "GET",
      success: function (response) {
          if (response) {
              // Set the values in the modal fields
              brandName.value = response.name || '';
              

              // Show the logo in the modal
              if (response.logo) {
                  const logoPreview = document.querySelector("#logoPreview");
                  if (logoPreview) {
                      logoPreview.src = `${rootUrl}media/${response.logo}`;
                      logoPreview.style.display = "block";
                  }
              }

              // Open the modal
              $('#viewBrandModal').modal('show');
          } else {
              console.error("Failed to load brand data.");
          }
      },
      error: function (response) {
          console.error("Failed to load brand data:", response);
      },
  });
}



// async function editBrandHandler() {
//   formdata.append("name", brandName.value);
//   formdata.append("logo", brandLogo.files[0]); 

//   $.ajax({
//       url: `/api/companies/${editBrandId}/`,
//       type: "PUT",
//       headers: {
//           "X-CSRFToken": csrftoken,
//       },
//       data: formdata,
//       processData: false,
//       contentType: false,
//       success: function (response) {
//           toastBody.textContent = "Brand updated successfully";
//           liveToast.classList.add("show");
//           getAllBrands();
//       },
//       error: function (response) {
//           toastBody.textContent = "Something went wrong";
//           liveToast.classList.add("show");
//       },
//   });
// }

// Delete brand handler
async function brandDeleteHandler(companyId) {
  $.ajax({
    url: `/api/companies/${companyId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response.status === "success") {
        getAllBrands();
        toastBody.textContent = "Brand deleted successfully";
        liveToast.classList.add("show");
      }
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";
      liveToast.classList.add("show");
    },
  });
}
