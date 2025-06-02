const haveMedHistory = document.querySelector("#haveMedHistory");
const haveRiskFactor = document.querySelector("#haveRiskFactor");

haveMedHistory.addEventListener("change", function (e) {
  
  if (e.target.checked) {
    document.querySelector("#midicine_history").style.display = "block";
  } else {
    document.querySelector("#midicine_history").style.display = "none";
  }
})
haveRiskFactor.addEventListener("change", function (e) {
  
  if (e.target.checked) {
    document.querySelector("#risk_factor").style.display = "block";
  } else {
    document.querySelector("#risk_factor").style.display = "none";
  }
})

const medicineNameClear = document.querySelector("#medicine_name_clear");
const dosageInstructionsClear = document.querySelector("#dosage_instr_clear");

const generalInstructionsClear = document.querySelector("#instruction_clear");
const adviceClear = document.querySelector("#advice_clear");
const testSearchClear = document.querySelector("#test_search_clear");

medicineNameClear.addEventListener("click", function () {
  document.getElementById("med_search").value = "";
});

dosageInstructionsClear.addEventListener("click", function () {
  document.getElementById("dosage_instruction").value = "";
});
generalInstructionsClear.addEventListener("click", function () {
  document.getElementById("instruction").value = "";
});
adviceClear.addEventListener("click", function () {
  document.getElementById("advice").value = "";
});
testSearchClear.addEventListener("click", function () {
  document.getElementById("test_search").value = "";
});


const followUpDuration = document.getElementById("follow_up_duration");
followUpDuration.addEventListener("change", function () {
  if (followUpDuration.value ) {
    document.getElementById("follow_up_unit").removeAttribute("disabled");
  } else{
    document.getElementById("follow_up_unit").setAttribute("disabled", "");
    document.getElementById("follow_up_unit").value = "0";
  }
});

const medicineDuration = document.getElementById("medicine_duration");
medicineDuration.addEventListener("change", function () {
  if (medicineDuration.value ) {
    document.getElementById("medicine_duration_unit").removeAttribute("disabled");
  }else{
    document.getElementById("medicine_duration_unit").setAttribute("disabled", "");
    document.getElementById("medicine_duration_unit").value = "0";
  }
});


const medicineSearchResultDiv = document.querySelector(
  "#medicine_search_result"
);
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
  const medicineName = document.getElementById("med_name").value;
  const strength = document.getElementById("med_strength").value;
  const dosage_form = document.getElementById("med_dosage_form").value;
  const dosage = document.getElementById("medicine_dosage").value;
  const dosageInstruction = document.querySelector("#dosage_instruction").value;
  const mealInstruction = document.getElementById(
    "medicine_meal_instruction"
  ).value;
  const duration = document.getElementById("medicine_duration").value;
  const durationOption = document.getElementById("medicine_duration_unit").value;
  const conditionalInstruction = document.getElementById(
    "instruction"
  ).value;

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

  if (dosage === "0") {
    document.querySelector(".dosage_error").textContent =
      "Please select a dosage";
    return;
  } else {
    document.querySelector(".dosage_error").textContent = "";
  }

  
  if (mealInstruction === "0") {
    document.querySelector(".meal_error").textContent =
      "Please select a Meal Instruction";
    return;
  } else {
    document.querySelector(".meal_error").textContent = "";
  }

  if (!duration) {
    document.querySelector(".duration_error").textContent =
      "Please select a medicine taking duration";
    return;
  } else {
    document.querySelector(".duration_error").textContent = "";
  }


  addedMedicine.innerHTML += `<tr>
                                <td>
                                    <span class="dosage_form-name">${dosage_form}</span>  
                                    <span class="medicine-name">${medicineName}</span> 
                                    <span class="medicine-strength">${strength}</span> 
                                </td>
                                <td>${dosage}</td>
                                <td>${dosageInstruction}</td>
                                <td>${mealInstruction}</td>
                                <td>${conditionalInstruction}</td>
                                <td>${duration} ${durationOption}</td>
                                <td class="text-end">
                                    <button class="btn btn-md rounded font-sm">aRemove</button>
                                </td>
                            </tr>`;

  medicines.push({
    dosage_form,
    medicineName,
    strength,
    dosage,
    dosageInstruction,
    mealInstruction,
    conditionalInstruction,
    duration,
  });

  removeMedicineHandler();
}

// remove medicine
function removeMedicineHandler() {
  const removeMedicineButtons =
    addedMedicine.querySelectorAll(".text-end button"); // Select the actual button, not the container
  removeMedicineButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent any default action
      e.stopPropagation(); // Stop the event from bubbling up
      this.closest("tr").remove(); // Remove only the closest parent row
    });
  });
}

// add medicine submit handler
const addMedicineFormBtn = document.querySelector(
  "#add_medicine_form_submit_btn"
);

document.querySelector("#add_medicine_form_clear_btn").addEventListener("click", () => {
  document.querySelector("#med_search").value = "";
  document.querySelector("#med_strength").value = "";
  document.querySelector("#med_dosage_form").value = "";
  document.querySelector("#medicine_dosage").value = "0";
  document.querySelector("#dosage_instruction").value = "";
  document.querySelector("#medicine_meal_instruction").value = "0";
  document.querySelector("#instruction").value = "";
  document.querySelector("#medicine_duration").value = "";
  document.querySelector("#medicine_duration_unit").value = "0";
})

const addMedicineForm = document.querySelector("#add_medicine_form");


addMedicineFormBtn.addEventListener("click", function (e) {
  e.preventDefault(); // Prevent the form from submitting
  e.stopPropagation(); // Stop the event from bubbling up if necessary

  addMedicineHandler();
  return false;
});

// scrollbar
const medicineList = document.querySelector("#medicine_lists");
const ps = new PerfectScrollbar(medicineList);



document
  .querySelector("#submit_prescription_btn")
  .addEventListener("click", function (e) {
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

  document.body.insertAdjacentHTML("beforeend", modalHtml);
  const errorModal = new bootstrap.Modal(document.getElementById("errorModal"));
  errorModal.show();
}

// video functionality
// Drag Functionality for video streams
function dragVideo() {
  let videoElement = document.getElementById("video-streams");

  let isDragging = false; // To track when the element is being dragged
  let startX, startY, initialTop, initialRight; // For storing initial positions

  videoElement.addEventListener("mousedown", (e) => {
    e.preventDefault();
    // Set dragging to true
    isDragging = true;

    // Get the initial positions
    startX = e.clientX;
    startY = e.clientY;
    initialTop = parseInt(window.getComputedStyle(videoElement).top);
    initialRight = parseInt(window.getComputedStyle(videoElement).right);

    console.log(
      "mousedown event has occured",
      startX,
      startY,
      initialTop,
      initialRight
    );
  });

  document.addEventListener("mousemove", (e) => {
    if (isDragging) {
      // Calculate how far the mouse has moved
      let deltaX = e.clientX - startX;
      let deltaY = e.clientY - startY;

      // Update the top and right values
      videoElement.style.top = initialTop + deltaY + "px";
      videoElement.style.right = initialRight - deltaX + "px";

      console.log(
        "mousemove event has occured",
        startX,
        e.clientX,
        deltaX,
        "|",
        startY,
        e.clientY,
        deltaY
      );
    }
  });

  document.addEventListener("mouseup", () => {
    // Stop dragging when the mouse is released
    isDragging = false;
  });
}

// agora crdentials
const APP_ID = "ae8218aff801440ba01d25cd22820230";

let localTracks = [];
let remoteUsers = {};
let client;
let joinAndDisplayLocalStream = async (channel, token) => {
  if (client) {
    await client.leave();
    client.removeAllListeners();
    client = null;
  }
  
  client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
  client.on("user-published", handleUserJoined);

  client.on("user-left", leaveAndRemoveLocalStream);

  
  let UID = await client.join(APP_ID, channel, token, null);

  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

  
  let player = `<div class="video-container" id="user-container-${UID}">
                        <div class="video-player" id="user-${UID}"></div>
                  </div>`;
  document
    .getElementById("video-streams2")
    .insertAdjacentHTML("beforeend", player);

  localTracks[1].play(`user-${UID}`);

  await client.publish([localTracks[0], localTracks[1]]);

  let element3 = document.querySelector(
    "#video-streams2 .video-container > div > div"
  );
  console.log(element3);
  if (element3) {
    element3.style.backgroundColor = "transparent";
  }

  let element4 = document.querySelector(
    "#video-streams2 .video-container > div > div video"
  );
  console.log(element4);
  if (element4) {
    element4.style.borderRadius = "10px";
  }
};

let joinTime;
let callEndTime;
let currentCallUser;
let currentCallPatient;
let callingId;
let callingGroup;
let joinStream = async (channel, token,group, user, ppno, calling_id) => {
  currentCallUser = user;
  callingGroup = group;
  callingId = calling_id;
  currentCallPatient=ppno;
  if(document.getElementById("video-streams2").children.length > 0){
    return;
  }
  console.log("calling_id",calling_id)
  let call_status = "in_progress"
  let call_id = callingId


    $.ajax({
      url: "/update-web-call/",
      type: 'POST',
      data: { 
        call_status: call_status,
        call_id: call_id,
      },
      success: function(response) {
              if (response.success) {
                  alert('Call ended successfully!');
              } else {
                  alert('Failed to Call ended: ' + response.error);
              }
          },
          error: function(xhr, status, error) {
              alert('An error occurred: ' + error);
          }
      });
  joinTime = Date.now();

  document.getElementById("video-streams").style.display = "block";

  dragVideo();
  document
    .getElementById("leave-btn")
    .addEventListener("click", () => {
      leaveAndRemoveLocalStream(callingId);
    });

  document.getElementById("mic-btn").addEventListener("click", function () {
    toggleMic(this);
  });
  document.getElementById("camera-btn").addEventListener("click", function () {
    toggleCamera(this);
  });

    if (group === "pharmacy") {
      document.getElementById(
        "patient_id"
      ).textContent = `Pateint: ${ppno}`;
      document.getElementById(
        "pharmacy_id"
      ).textContent = `Pharmacy: ${user}`;
    } else {
      document.getElementById(
        "patient_id"
      ).textContent = `Pateint: ${user}`;
    }

    await joinAndDisplayLocalStream(channel, token);
  
  // document.getElementById("join-btn")ft.style.display = "none";
  // document.getElementById('stream-controls').style.display = 'flex'
};

let handleUserJoined = async (user, mediaType) => {
  remoteUsers[user.uid] = user;
  console.log(Object.keys(remoteUsers).length)
  await client.subscribe(user, mediaType);

  if (mediaType === "video") {
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player != null) {
      player.remove();
    }

    player = `<div class="video-container" id="user-container-${user.uid}">
                        <div class="video-player" id="user-${user.uid}"></div> 
                 </div>`;
    document
      .getElementById("video-streams")
      .insertAdjacentHTML("beforeend", player);

    user.videoTrack.play(`user-${user.uid}`);

    let element1 = document.querySelector(
      "#video-streams > .video-container > div > div"
    );
    if (element1) {
      element1.style.backgroundColor = "transparent";
    }

    let element2 = document.querySelector(
      "#video-streams > .video-container > div > div video"
    );
    if (element2) {
      element2.style.borderRadius = "10px";
    }
  }

  if (mediaType === "audio") {
    user.audioTrack.play();
  }
};

let leaveAndRemoveLocalStream = async (callingId) => {
  let call_status = "ended"
  let call_id = callingId

  callEndTime = Date.now();
  console.log(
    "duration: " +
      ((callEndTime - joinTime) / 1000 / 60).toFixed(2) +
      " minutes"
  );

  console.log("userleft");
  await client.leave();
  // document.getElementById("join-btn").style.display = "block";
  document.getElementById("stream-controls").style.display = "none";
  document.getElementById("video-streams").style.display = "none";
  document.getElementById("video-streams").innerHTML = "";
  document.getElementById(
    "video-streams"
  ).innerHTML = `<div class="video__options__wrapper position-relative">
                        <div id="stream-controls"
                            class="video__options position-absolute d-flex align-items-center justify-content-center gap-2"
                            style="top: 190px; left: 0px; width: 100%; z-index: 300;">
                            <button
                            id="camera-btn"
                                class="border-0 rounded-circle bg-white d-flex justify-content-center align-items-center"
                                style="width: 40px; height: 40px;"><i
                                    class="material-icons md-videocam text-body"></i></button>
                            <button
                            id="mic-btn"
                                class="border-0 rounded-circle bg-white d-flex justify-content-center align-items-center"
                                style="width: 40px; height: 40px;"><i
                                    class="material-icons md-volume_up text-body"></i></button>
                            <button
                            id="leave-btn"
                                class="border-0 rounded-circle bg-white d-flex justify-content-center align-items-center"
                                style="width: 40px; height: 40px;"><i
                                    class="material-icons md-call text-danger"></i></button>
                        </div>
                    </div>
                    
                        <div id="video-streams2"></div>
                    `;

  $.ajax({ 
    url: "/update-web-call/",
    type: 'POST',
    data: { 
      call_status: call_status,
      call_id: call_id,
    },
    success: function(response) {
            if (response.success) {
                alert('Call ended successfully!');
            } else {
                alert('Failed to Call ended: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('An error occurred: ' + error);
        }
    });

  for (let i = 0; localTracks.length > i; i++) {
    localTracks[i].stop();
    localTracks[i].close();
  }

  
};

let toggleMic = async (clickedElement) => {
  if (localTracks[0].muted) {
    await localTracks[0].setMuted(false);
    clickedElement.querySelector("i").classList.remove("md-volume_off");
    clickedElement.querySelector("i").classList.add("md-volume_up");
  } else {
    await localTracks[0].setMuted(true);
    clickedElement.querySelector("i").classList.add("md-volume_off");
    clickedElement.querySelector("i").classList.remove("md-volume_up");
  }
};

let toggleCamera = async (clickedElement) => {
  if (localTracks[1].muted) {
    await localTracks[1].setMuted(false);
    clickedElement.querySelector("i").classList.remove("md-videocam_off");
    clickedElement.querySelector("i").classList.add("md-videocam");
  } else {
    await localTracks[1].setMuted(true);
    clickedElement.querySelector("i").classList.remove("md-videocam");
    clickedElement.querySelector("i").classList.add("md-videocam_off");
  }
};


function submitPrescription() {

  if(!document.getElementById("problem").value){
    alert("Please write chief complain");
    return;
  }

  const medicines = Array.from(
    document.querySelectorAll("#added_medicines tr")
  ).map((row) => {
    const medicineName = row.querySelector(".medicine-name").textContent.trim();
    const strength = row.querySelector(".medicine-strength").textContent.trim();
    const dosage_form_name = row
      .querySelector(".dosage_form-name")
      .textContent.trim(); 
    const dosage = row.querySelectorAll("td")[1].textContent.trim();
    const dosageInstruction = row.querySelectorAll("td")[2].textContent.trim();
    const mealInstruction = row.querySelectorAll("td")[3].textContent.trim();
    const conditionalInstruction = row
      .querySelectorAll("td")[4]
      .textContent.trim();
    const duration = row.querySelectorAll("td")[5].textContent.trim();

    return {
      medicineName,
      strength,
      dosage_form_name,
      dosage,
      mealInstruction,
      conditionalInstruction,
      duration,
      dosageInstruction
    };
  });

  if(medicines.length === 0) {
    alert("Please add a medicine at least");
    return;
  }

  const selectedTestsElement = document.getElementById("selected_tests");

  console.log("selectedTestsElement",selectedTestsElement)

  let selectedTests = selectedTestsElement ? selectedTestsElement.value : null;
  if (selectedTests === "") {
    selectedTests = null;
  }

  let followupDate = document.getElementById("follow_up_duration").value;
  if (followupDate === "") {
    followupDate = null;
  }
let followupDuration = document.getElementById("follow_up_unit").value;
  const prescriptionData = {
    user: currentCallUser,
    ppno: currentCallPatient,
    calling_id: callingId,
    call_duration: ((callEndTime - joinTime) / 1000 / 60).toFixed(2) +
    " minutes",
    patient_name: document.getElementById("patient_name").value,
    patient_age: document.getElementById("patient_age").value,
    patient_gender: document.querySelector("input[name='gender']").value,
    medicine_history: document.getElementById("midicine_history").value,
    risk_factor: document.getElementById("risk_factor").value,
    problem: document.getElementById("problem").value,
    advice: document.getElementById("advice").value,
    followup: `${followupDate} ${followupDuration}`,
    medicines: medicines,
    selected_tests: selectedTests,
    group: callingGroup,
  };

  console.log(prescriptionData);

  fetch(`/assign_prescription/`, {
    method: "POST",
    body: JSON.stringify(prescriptionData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        window.location.href = "/prescription/patients_list/";
      } else {
        showErrorModal(data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while creating the prescription.");
    });
}
