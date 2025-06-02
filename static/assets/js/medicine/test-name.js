const testNameName = document.querySelector("#testName_name");
const testNameCategory = document.querySelector("#testName_category");
const liveTestNameToast = document.querySelector("#liveTestNameToast");
const toastBody = document.querySelector("#liveTestNameToast .toast-body");
const testNameContainer = document.querySelector("#testName_container");
const rootUrl = "http://127.0.0.1:8000";
let testNameFormType = "add";
let edittestNameId;

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

// testName submit handler
function testNameSubmitHandler() {
  console.log(testNameFormType);
  if (testNameFormType === "add") {
    addNewtestNameHandler();
  } else {
    edittestNameHandler();
  }
}

// add testName function
async function addNewtestNameHandler() {
  if (!testNameName.value) {
    document.querySelector(".testName_name_error").textContent =
      "please enter a name";
    return;
  }
  if (!testNameCategory.value || testNameCategory.value === "0") {
    document.querySelector(".testName_category_error").textContent =
      "please enter a category";
    return;
  }
  formdata.append("name", testNameName.value);
  formdata.append("test_cat_name", testNameCategory.value);

  $.ajax({
    url: "/api/test-names/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
      if (response.status === "success") {
        testNameName.value = "";
        document.querySelector(".testName_name_error").textContent = "";
        document.querySelector(".testName_category_error").textContent = "";
        toastBody.textContent = "testName created successfully";

        liveTestNameToast.classList.add("show");
        getAllTestNames();
      } else {
        toastBody.textContent = "Something went wrong";

        liveTestNameToast.classList.add("show");
      }
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveTestNameToast.classList.add("show");
    },
  });
}

// get all TestNames function
async function getAllTestNames() {
  $.ajax({
    url: "/api/test-names/",
    type: "GET",
    success: function (response) {
      console.log(response);
      testNameContainer.innerHTML = "";

      response.map((item) => {
        testNameContainer.innerHTML += `<article class="itemlist">
                <div class="row align-items-center">
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <h6 class="mb-0">${item.name}</h6>
                        </div>
                    </div>
                    <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
                        <div class="info">
                            <span class="mb-0">${item.test_cat_name__name}</span>
                        </div>
                    </div>
                    <div class="col-lg-2 col-sm-2 col-4 col-action text-end d-flex gap-3 mr-10">
                        <a data-bs-toggle="modal" data-bs-target="#viewTestNameModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                            Edit </a>
                        <a onclick="testNameDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
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
getAllTestNames();

// function show edit modal
function showEditModal(id) {
  testNameFormType = "edit";
  edittestNameId = id;
  $.ajax({
    url: `/api/test-names/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        testNameName.value = response.name || "";
        testNameCategory.value = response.test_cat_id || "";
      } else {
        console.error("Failed to load testName data.");
      }
    },
    error: function (response) {
      console.error("Failed to load testName data:", response);
    },
  });
}

// function show edit modal
function hideEditModal() {
  testNameFormType = "add";
  edittestNameId = "";
  testNameName.value = "";
}

// edittestNamehandler
async function edittestNameHandler() {
  if (!testNameName.value) {
    document.querySelector(".testName_name_error").textContent =
      "please enter a name";
    return;
  }
  if (!testNameCategory.value || testNameCategory.value === "0") {
    document.querySelector(".testName_category_error").textContent =
      "please enter a category";
    return;
  }
  if (testNameName.value) {
    formdata.set("name", testNameName.value);
  }
  if (testNameCategory.value) {
    formdata.set("test_cat_name", testNameCategory.value);
  }

  if (!edittestNameId) {
    return;
  }

  $.ajax({
    url: `/api/test-names/${edittestNameId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllTestNames();
        edittestNameId = "";
        testNameFormType = "add";
        testNameName.value = "";
        testNameCategory.value = "";
        document.querySelector(".testName_name_error").textContent = "";
        document.querySelector(".testName_category_error").textContent = "";
        toastBody.textContent = "testName updated successfully";
        liveTestNameToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveTestNameToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveTestNameToast.classList.add("show");
      }
    },
  });
}

// deletetestNamehandler
async function testNameDeleteHandler(testNameId) {
  $.ajax({
    url: `/api/test-names/${testNameId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllTestNames();
        toastBody.textContent = "testName deleted successfully";
        liveTestNameToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveTestNameToast.classList.add("show");
      }
    },
  });
}
