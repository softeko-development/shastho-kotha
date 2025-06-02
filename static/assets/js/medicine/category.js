const categoryName = document.querySelector("#category_name");
const liveCategoryToast = document.querySelector("#liveCategoryToast");
const toastBody = document.querySelector("#liveCategoryToast .toast-body");
const categoryContainer = document.querySelector("#category_container");
const rootUrl = "http://127.0.0.1:8000";
let categoryFormType = "add";
let editcategoryId;

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

// category submit handler
function categorySubmitHandler() {
  if (categoryFormType === "add") {
    addNewcategoryHandler();
  } else {
    editcategoryHandler();
  }
}

// add category function
async function addNewcategoryHandler() {
  if(!categoryName.value){
    document.querySelector(".category_name_error").textContent = "please enter a name";
    return;
  }
  formdata.append("name", categoryName.value);

  $.ajax({
    url: "/api/categories/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
        categoryName.value = ""
        document.querySelector(".category_name_error").textContent = "";
      toastBody.textContent = "category created successfully";

      liveCategoryToast.classList.add("show");
      getAllCategorys();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveCategoryToast.classList.add("show");
    },
  });
}

// get all Categorys function
async function getAllCategorys() {
  $.ajax({
    url: "/api/categories/",
    type: "GET",
    success: function (response) {
      categoryContainer.innerHTML = "";

      response.map((item) => {
        categoryContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.name}</h6>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewCategoryModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="categoryDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
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
getAllCategorys();

// function show edit modal
function showEditModal(id) {
  categoryFormType = "edit";
  editcategoryId = id;
  $.ajax({
    url: `/api/categories/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        categoryName.value = response.name || "";
      } else {
        console.error("Failed to load category data.");
      }
    },
    error: function (response) {
      console.error("Failed to load category data:", response);
    },
  });
}


// function show edit modal
function hideEditModal() {
    categoryFormType = "add";
    editcategoryId = "";
    categoryName.value = ""
}



// editcategoryhandler
async function editcategoryHandler() {
  if(!categoryName.value){
    document.querySelector(".category_name_error").textContent = "please enter a name";
    return;
  }
  if (categoryName.value) {
    formdata.set("name", categoryName.value);
  }

  if(!editcategoryId){
    return;
  }

  $.ajax({
    url: `/api/categories/${editcategoryId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllCategorys();
        editcategoryId = "";
        categoryFormType = "add";
        categoryName.value = "";
        document.querySelector(".category_name_error").textContent = "";
        toastBody.textContent = "category updated successfully";
        liveCategoryToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveCategoryToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveCategoryToast.classList.add("show");
      }
    },
  });
}

// deletecategoryhandler
async function categoryDeleteHandler(companyId) {
  $.ajax({
    url: `/api/categories/${companyId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllCategorys();      
        toastBody.textContent = "category deleted successfully";
        liveCategoryToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveCategoryToast.classList.add("show");
      }
    },
  });
}
