const productCode = document.querySelector("#product_code");
const productName = document.querySelector("#product_name");
const productStrength = document.querySelector("#product_strength");
const productCategory = document.querySelector("#product_category");
const productCompany = document.querySelector("#product_company");
const productGeneric = document.querySelector("#product_generic");
const productDosage = document.querySelector("#product_dosage");
const liveProductToast = document.querySelector("#liveProductToast");
const toastBody = document.querySelector("#liveProductToast .toast-body");
const productContainer = document.querySelector(
  "#product_container table tbody"
);
const rootUrl = "http://127.0.0.1:8000";
let productFormType = "add";
let editproductId;

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

// product submit handler
function productSubmitHandler() {
  console.log(productFormType);
  if (productFormType === "add") {
    addNewproductHandler();
  } else {
    editproductHandler();
  }
}

// add product function
async function addNewproductHandler() {
  if (!productCode.value) {
    document.querySelector(".product_code_error").textContent =
      "please enter a code";
    return;
  }
  if (!productName.value) {
    document.querySelector(".product_name_error").textContent =
      "please enter a name";
    return;
  }
  if (!productStrength.value) {
    document.querySelector(".product_strength_error").textContent =
      "please enter a strength";
    return;
  }
  if (!productCategory.value || productCategory.value === "0") {
    document.querySelector(".product_category_error").textContent =
      "please enter a category";
    return;
  }
  if (!productCompany.value || productCompany.value === "0") {
    document.querySelector(".product_company_error").textContent =
      "please enter a company name";
    return;
  }
  if (!productGeneric.value || productGeneric.value === "0") {
    document.querySelector(".product_generic_error").textContent =
      "please enter a generic name";
    return;
  }
  if (!productDosage.value || productDosage.value === "0") {
    document.querySelector(".product_dosage_error").textContent =
      "please enter a dosage";
    return;
  }

  formdata.append("item_code", productCode.value);
  formdata.append("name", productName.value);
  formdata.append("strength", productStrength.value);
  formdata.append("category", productCategory.value);
  formdata.append("pharmaceutical_com_id", productCompany.value);
  formdata.append("generics_id", productGeneric.value);
  formdata.append("dosage_form_id", productDosage.value);

  $.ajax({
    url: "/api/products/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false, // Prevent jQuery from converting data to query string
    contentType: false, // Required to handle multipart/form-data
    success: function (response) {
      if (response.status === "success") {
        productName.value = "";
        document.querySelector(".product_code_error").textContent = "";
        document.querySelector(".product_name_error").textContent = "";
        document.querySelector(".product_strength_error").textContent = "";
        document.querySelector(".product_category_error").textContent = "";
        document.querySelector(".product_company_error").textContent = "";
        document.querySelector(".product_generic_error").textContent = "";
        document.querySelector(".product_dosage_error").textContent = "";
        toastBody.textContent = "product created successfully";

        liveProductToast.classList.add("show");
        getAllProducts();
      } else {
        toastBody.textContent = "Something went wrong";

        liveProductToast.classList.add("show");
      }
    },
    error: function (response) {
      toastBody.textContent = "Something went wrong";

      liveProductToast.classList.add("show");
    },
  });
}

// get all Products function
async function getAllProducts() {
  $.ajax({
    url: "/api/products/",
    type: "GET",
    success: function (response) {
      console.log(response);
      productContainer.innerHTML = "";

      response.map((item) => {
        productContainer.innerHTML += `<tr>
                        <td>${item.item_code}</td>
                        <td>${item.name}</td>
                        <td>${item.strength}</td>
                        <td>${item.category__name}</td>
                        <td>${item.pharmaceutical_com_id__name}</td>
                        <td>${item.generics_id__name}</td>
                        <td>${item.dosage_form_id__name}</td>
                        <td class="text-end">
                            <div class="d-flex justify-content-end gap-3">
                                <a data-bs-toggle="modal" data-bs-target="#viewProductModal" onclick="showEditModal(${item.id})" class="btn btn-sm font-sm rounded btn-brand"> <i class="material-icons md-edit"></i>
                                    Edit </a>
                                <a onclick="productDeleteHandler(${item.id})" class="btn btn-sm font-sm btn-light rounded"> <i
                                        class="material-icons md-delete_forever"></i> Delete </a>
                            </div>
                        </td>
                    </tr>`;
      });
    },
    error: function (response) {
      console.error(response.errors);
    },
  });
}
getAllProducts();

// function show edit modal
function showEditModal(id) {
  productFormType = "edit";
  editproductId = id;
  $.ajax({
    url: `/api/products/${id}/`,
    type: "GET",
    success: function (response) {
      if (response) {
        productCode.value = response.item_code || "";
        productName.value = response.name || "";
        productStrength.value = response.strength || "";
        productCategory.value = response.category || "";
        productCompany.value = response.company || "";
        productGeneric.value = response.generic || "";
        productDosage.value = response.dosage || "";
      } else {
        console.error("Failed to load product data.");
      }
    },
    error: function (response) {
      console.error("Failed to load product data:", response);
    },
  });
}

// function show edit modal
function hideEditModal() {
  productFormType = "add";
  editproductId = "";
  productCode.value = "";
  productName.value = "";
  productStrength.value = "";
  productCategory.value = "";
  productCompany.value = "";
  productGeneric.value = "";
  productDosage.value = "";
}

// editproducthandler
async function editproductHandler() {
  if (!productCode.value) {
    document.querySelector(".product_code_error").textContent =
      "please enter a code";
    return;
  }
  if (!productName.value) {
    document.querySelector(".product_name_error").textContent =
      "please enter a name";
    return;
  }
  if (!productStrength.value) {
    document.querySelector(".product_strength_error").textContent =
      "please enter a strength";
    return;
  }
  if (!productCategory.value || productCategory.value === "0") {
    document.querySelector(".product_category_error").textContent =
      "please enter a category";
    return;
  }
  if (!productCompany.value || productCompany.value === "0") {
    document.querySelector(".product_company_error").textContent =
      "please enter a company name";
    return;
  }
  if (!productGeneric.value || productGeneric.value === "0") {
    document.querySelector(".product_generic_error").textContent =
      "please enter a generic name";
    return;
  }
  if (!productDosage.value || productDosage.value === "0") {
    document.querySelector(".product_dosage_error").textContent =
      "please enter a dosage";
    return;
  }

  formdata.set("item_code", productCode.value);
  formdata.set("name", productName.value);
  formdata.set("strength", productStrength.value);
  formdata.set("category", productCategory.value);
  formdata.set("pharmaceutical_com_id", productCompany.value);
  formdata.set("generics_id", productGeneric.value);
  formdata.set("dosage_form_id", productDosage.value);

  if (!editproductId) {
    return;
  }

  $.ajax({
    url: `/api/products/${editproductId}/`,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    processData: false,
    contentType: false,
    success: function (response) {
      if (response.status === "success") {
        getAllProducts();
        editproductId = "";
        productFormType = "add";
        productCode.value = "";
        productName.value = "";
        productStrength.value = "";
        productCategory.value = "";
        productCompany.value = "";
        productGeneric.value = "";
        productDosage.value = "";
        document.querySelector(".product_code_error").textContent = "";
        document.querySelector(".product_name_error").textContent = "";
        document.querySelector(".product_strength_error").textContent = "";
        document.querySelector(".product_category_error").textContent = "";
        document.querySelector(".product_company_error").textContent = "";
        document.querySelector(".product_generic_error").textContent = "";
        document.querySelector(".product_dosage_error").textContent = "";
        toastBody.textContent = "product updated successfully";
        liveProductToast.classList.add("show");
      } else {
        toastBody.textContent = "Something went wrong";
        liveProductToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveProductToast.classList.add("show");
      }
    },
  });
}

// deleteproducthandler
async function productDeleteHandler(productId) {
  $.ajax({
    url: `/api/products/${productId}/`,
    type: "DELETE",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    success: function (response) {
      if (response) {
        getAllProducts();
        toastBody.textContent = "product deleted successfully";
        liveProductToast.classList.add("show");
      }
    },
    error: function (response) {
      if (response) {
        toastBody.textContent = "Something went wrong";
        liveProductToast.classList.add("show");
      }
    },
  });
}
