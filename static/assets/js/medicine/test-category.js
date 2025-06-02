const testCategoryName = document.querySelector("#testCategory_name");
const liveTestCategoryToast = document.querySelector("#liveTestCategoryToast");
const toastBody = document.querySelector("#liveTestCategoryToast .toast-body");
const testCategoryContainer = document.querySelector("#testCategory_container");
const rootUrl = "http://127.0.0.1:8000";
let testCategoryFormType = "add";
let edittestCategoryId;

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

// testCategory submit handler
function testCategorySubmitHandler() {
  if (testCategoryFormType === "add") {
    addNewtestCategoryHandler();
  } else {
    edittestCategoryHandler();
  }
}

// add testCategory function
async function addNewtestCategoryHandler() {
  if(!testCategoryName.value){
    document.querySelector(".testCategory_name_error").textContent = "please enter a name";
    return;
  }
  formdata.append("name", testCategoryName.value);

  $.ajax({
    url: "/api/test-categories/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
        testCategoryName.value = ""
        document.querySelector(".testCategory_name_error").textContent = "";
      toastBody.textContent = "testCategory created successfully";

      liveTestCategoryToast.classList.add("show");
      getAllTestCategorys();
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveTestCategoryToast.classList.add("show");
    },
  });
}

// get all TestCategorys function
async function getAllTestCategorys() {
  $.ajax({
    url: "/api/test-categories/",
    type: "GET",
    success: function (response) {
      testCategoryContainer.innerHTML = "";

      response.map((item) => {
        testCategoryContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.name}</h6>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewTestCategoryModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="testCategoryDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
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
getAllTestCategorys();

// function show edit modal
function showEditModal(id) {
  testCategoryFormType = "edit";
  edittestCategoryId = id;
  $.ajax({
    url: `/api/test-categories/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        testCategoryName.value = response.name || "";
      } else {
        console.error("Failed to load testCategory data.");
      }
    },
    error: function (response) {
      console.error("Failed to load testCategory data:", response);
    },
  });
}


// function show edit modal
function hideEditModal() {
    testCategoryFormType = "add";
    edittestCategoryId = "";
    testCategoryName.value = ""
}



// edittestCategoryhandler
async function edittestCategoryHandler() {
  if(!testCategoryName.value){
    document.querySelector(".testCategory_name_error").textContent = "please enter a name";
    return;
  }
  if (testCategoryName.value) {
    formdata.set("name", testCategoryName.value);
  }

  if(!edittestCategoryId){
    return;
  }

  $.ajax({
    url: `/api/test-categories/${edittestCategoryId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllTestCategorys();
        edittestCategoryId = "";
        testCategoryFormType = "add";
        testCategoryName.value = "";
        document.querySelector(".testCategory_name_error").textContent = "";        
        toastBody.textContent = "testCategory updated successfully";
        liveTestCategoryToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveTestCategoryToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveTestCategoryToast.classList.add("show");
      }
    },
  });
}

// deletetestCategoryhandler
async function testCategoryDeleteHandler(testCategoryId) {
  $.ajax({
    url: `/api/test-categories/${testCategoryId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllTestCategorys();      
        toastBody.textContent = "testCategory deleted successfully";
        liveTestCategoryToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveTestCategoryToast.classList.add("show");
      }
    },
  });
}
