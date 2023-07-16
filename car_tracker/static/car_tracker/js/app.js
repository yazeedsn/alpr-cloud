// ------------------------------ navbar functionality ----------------------------------------

const dashboardSideNav = document.querySelector('.dashboard_sidenav');
const trackSideNav = document.querySelector('.track_sidenav');
let activeTab = "about";


document.addEventListener("DOMContentLoaded", initializeTabs);


// ------------------------------ dashboard tab functionality ----------------------------------------

const addDeviceBtn = document.getElementById('add-device-btn');
const closePopupButton = document.getElementById('close-popup-button');
const deviceTypeSelect = document.getElementById('device-type');
const confirmDeviceBtn = document.getElementById('confirm-device-btn');
const addDevicePopup = document.getElementById('add-device-popup');
const removeButtons = document.querySelectorAll('.remove-device-btn');
const deviceIdGroup = document.querySelector('.device-id-group');
const recordingTimeGroup = document.querySelector('.recording-time-group');
const fileGroup = document.querySelector('.file-group');
const cameraStream = document.getElementById('camera-stream');


addDeviceBtn.addEventListener('click', showPopupWindow);
closePopupButton.addEventListener('click', hidePopupWindow);
confirmDeviceBtn.addEventListener('click',  handleNewDevice);


// ------------------------------ tracking tab functionality ----------------------------------------

const filterBtn = document.getElementById('filter-btn');
const deviceList = document.getElementById('device-list');
const trackInputField = document.getElementById('track-input-field');
const startTimeInputField = document.getElementById('start-time-input-field');
const endTimeInputField = document.getElementById('end-time-input-field');
const timeHeader = document.querySelector('#track-table th:nth-child(3)');
const filterButton = document.getElementById('filter-btn');
const resetButton = document.getElementById('reset-btn');
let isTimeSortedAscending = false;
let chevronDirection = '▲';


addChevronToTimeHeader();
trackInputField.addEventListener('keydown', handlePressingEnter);
deviceList.addEventListener('click', deleteEntry);
timeHeader.addEventListener('click', handleTimeHeaderClick);
filterButton.addEventListener('click', applyFilters);
resetButton.addEventListener('click', resetFilters);


// ----------------------------------------------------------------------------------------------------
//                                      navbar functions
// ----------------------------------------------------------------------------------------------------

function initializeTabs() {
    const tabLinks = document.getElementsByClassName("topnav")[0].getElementsByTagName("a");

    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].addEventListener("click", handleTabClick);
    }

    showContent(activeTab);
    toggleSideNavContent(activeTab);
    licensePlatesData = JSON.parse(licensePlates);
    fillLicensePlatesTable(licensePlatesData);
    fillDevicesList(licensePlatesData);
}

function fillLicensePlatesTable(licensePlates) {  
    appendResultsToTrackTable(licensePlates);
}

function fillDevicesList(licensePlates) {
    const deviceIds = new Set();
    for (const plate of licensePlates) {
        if (!deviceIds.has(plate.device_identifier)) {
            deviceIds.add(plate.device_identifier);
        }
    }

    for (const id of deviceIds) {
        createDeviceEntry(id);
    }
}

function handleTabClick(event) {
    event.preventDefault();

    const targetTab = event.target.getAttribute("href").substring(1);

    activeTab = targetTab;

    showContent(targetTab);
    toggleSideNavContent(targetTab);
}

function showContent(tab) {
    const contentContainers = document.getElementsByClassName("content");

    for (let i = 0; i < contentContainers.length; i++) {
        const container = contentContainers[i];

        const tabName = container.getAttribute("class").split(" ")[1].split("_")[0];

        if (tabName === tab) {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    }
}

function toggleSideNavContent(activeTab) {
    if (activeTab === 'about') {
        dashboardSideNav.style.display = 'none';
        trackSideNav.style.display = 'none';
    } else if (activeTab === 'dashboard') {
        dashboardSideNav.style.display = 'none';
        trackSideNav.style.display = 'none';
    } else if (activeTab === 'track') {
        dashboardSideNav.style.display = 'none';
        trackSideNav.style.display = 'flex';
    }
}


// ----------------------------------------------------------------------------------------------------
//                                      dashboard functions
// ----------------------------------------------------------------------------------------------------

function showPopupWindow() {
    addDevicePopup.style.display = 'block';
}

function hidePopupWindow() {
    addDevicePopup.style.display = 'none';
}

function startCameraStream() {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        cameraStream.srcObject = stream;
      })
      .catch((error) => {
        console.error('Error accessing camera:', error);
      });
}
  
// Function to stop the camera stream
function stopCameraStream() {
    const mediaStream = cameraStream.srcObject;
    if (mediaStream) {
        const tracks = mediaStream.getTracks();
        tracks.forEach((track) => track.stop());
    }
}

// current time in HH:MM format
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

function handleNewDevice(event) {
    event.preventDefault();

    // Get form input values
    const deviceType = deviceTypeSelect.value;
    const deviceId = document.getElementById('device-id').value;
    const deviceName = document.getElementById('device-name').value;
    const recordingTime = document.getElementById('recording-time').value;
    const deviceLocation = document.getElementById('device-location').value;
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];

    if (deviceType === '' || deviceId === '' || deviceName === '') {
        alert('Error: Please fill in all required fields.');
        return;
    }

    // Create the device object
    const device = {
        deviceType,
        deviceId,
        deviceName,
        recordingTime,
        deviceLocation,
        file
    };

    // Add the device to the table
    addDeviceToTable(device);

    const popup = document.getElementById('add-device-popup');
    popup.style.display = 'none';

    // Send the device data to the server
    sendDataToServer(device);
}

function addDeviceToTable(device) {
    const tableBody = document.getElementById('table-body');

    // Create a new table row
    const row = document.createElement('tr');

    // Create table cells for each data field
    const deviceNameCell = document.createElement('td');
    deviceNameCell.textContent = device.deviceName;
    row.appendChild(deviceNameCell);

    const deviceIdCell = document.createElement('td');
    deviceIdCell.textContent = device.deviceId;
    deviceIdCell.classList.add('device-id');
    row.appendChild(deviceIdCell);

    const deviceTypeCell = document.createElement('td');
    deviceTypeCell.textContent = device.deviceType;
    row.appendChild(deviceTypeCell);

    const timeAddedCell = document.createElement('td');
    const currentTime = new Date().toLocaleString();
    timeAddedCell.textContent = currentTime;
    row.appendChild(timeAddedCell);

    const deviceLocationCell = document.createElement('td');
    deviceLocationCell.textContent = device.deviceLocation;
    row.appendChild(deviceLocationCell);

    const actionCell = document.createElement('td');
    const disconnectButton = document.createElement('button');
    disconnectButton.textContent = 'Remove';
    disconnectButton.classList.add('disconnect-device-btn');
    disconnectButton.classList.add('remove-device-btn');
    disconnectButton.addEventListener('click', () => { 
        const deviceRow = disconnectButton.closest('tr');
        remove_device(deviceRow) 
    });
    actionCell.appendChild(disconnectButton);
    row.appendChild(actionCell);

    tableBody.insertBefore(row, tableBody.firstChild);
}

removeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const row = button.closest('tr');
        row.remove();
        remove_device(row);
    });
});

function remove_device(deviceRow) {
    const deviceId = deviceRow.querySelector('.device-id').textContent;

    const csrfToken = getCookie('csrftoken');

    fetch(`${removeDeviceUrl}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            device_id: deviceId,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            deviceRow.remove();
        } else {
            console.error('Failed to remove device:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function sendDataToServer(device) {
    const formData = new FormData();
    formData.append('deviceType', device.deviceType);
    formData.append('deviceId', device.deviceId);
    formData.append('deviceName', device.deviceName);
    formData.append('recordingTime', device.recordingTime);
    formData.append('deviceLocation', device.deviceLocation);
    formData.append('file', device.file);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`${uploadFileUrl}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    })
    .then((jsonResponse) => {
        if (device.deviceType == 'image') {
            appendResultsToTrackTable(jsonResponse.results);
        } else if (device.deviceType == 'video' && jsonResponse.startedProcessing) {
            startPeriodicDataRetrieval(device.deviceId);
        }
        createDeviceEntry(device.deviceId);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function startPeriodicDataRetrieval(deviceId) {
    const url = getDeviceDataUrl.replace('__device_id__', deviceId);
    const intervalId = setInterval(() => {
        fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Request failed');
            }
            return response.json();
        })
        .then((jsonResponse) => {
            const transformedResults = transformResultsFormat(jsonResponse.results);
            appendResultsToTrackTable(transformedResults);
            if (jsonResponse.finishedProcessing) {
                clearInterval(intervalId);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, 10000);
}

function transformResultsFormat(results) {
    const transformedResults = [];
    results.forEach(subList => {
        subList.forEach(item => {
            transformedResults.push(item);
        });
    });
    return transformedResults;
}

// ----------------------------------------------------------------------------------------------------
//                                      track functions
// ----------------------------------------------------------------------------------------------------


function handlePressingEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        trackBtn.click();
    }
}

function createLicensePlateEntry(plateNumber) {
    const entry = document.createElement('li');
    entry.classList.add('device-entry');
    entry.classList.add('normal');

    const plateNumberText = document.createElement('span');
    plateNumberText.textContent = plateNumber;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.classList.add('delete-button');

    entry.appendChild(plateNumberText);
    entry.appendChild(deleteButton);

    deviceList.appendChild(entry);
}

function deleteEntry(event) {
    if (event.target.classList.contains('delete-button')) {
        const entry = event.target.parentNode;
        const deviceId = entry.querySelector('.deviceId').textContent;
    
        // Remove entry from side navigation
        entry.remove();
    
        // Clear track table entries with the same license plate number
        const trackTableBody = document.getElementById('track-table');
        const entries = trackTableBody.querySelectorAll('.license-plate-entry');
    
        entries.forEach(entry => {
            const deviceIdCell = entry.querySelector('.deviceId');
            if (deviceIdCell) {
                if (deviceIdCell.textContent === deviceId) {
                    entry.remove();
                }
            } else {
                console.error('Error: deviceIdCell is null');
            }
        });
    }
}

function appendResultsToTrackTable(results) {
    const trackTableBody = document.getElementById('track-table-body');
    const rows = Array.from(trackTableBody.getElementsByTagName('tr'));

    results.forEach((result, index) => {
        const {
            license_plate_id,
            plate_number,
            confidence_score,
            image_data,
            time,
            device_identifier,
            location,
        } = result;

        // Check if an entry for the same plate number from the same device within 1 minute already exists
        const duplicateExists = rows.some(row => {
            const rowDeviceId = row.querySelector('.deviceId').textContent;
            const rowPlateNumber = row.querySelector('.license-plate-number span').textContent;
            const rowTime = new Date(row.cells[2].textContent).getTime();
            const resultTime = new Date(time).getTime();

            const isSamePlateNumber = rowPlateNumber === plate_number;
            const isSameDevice = rowDeviceId === device_identifier;
            const isWithinOneMinute = Math.abs(rowTime - resultTime) <= 60000; // 1 minute = 60,000 milliseconds

            return isSamePlateNumber && isSameDevice && isWithinOneMinute;
        });

        if (duplicateExists) {
            return; // Skip adding the duplicate entry
        }

        const row = createRow();

        const idCell = createCell(license_plate_id);
        const deviceIdCell = createCell(device_identifier);
        deviceIdCell.classList.add("deviceId");
        const formattedTime = new Date(time).toLocaleString();
        const timeCell = createCell(formattedTime);

        const licensePlateCell = document.createElement('td');
        const licensePlateText = document.createElement('span');
        licensePlateText.textContent = plate_number;
        licensePlateCell.classList.add('license-plate-number');
        licensePlateCell.appendChild(licensePlateText);

        const vehicleTypeCell = createVehicleTypeCell(plate_number);
        const locationCell = createCell(location);
        const imageCell = createImageCell(image_data);

        row.appendChild(idCell);
        row.appendChild(deviceIdCell);
        row.appendChild(timeCell);
        row.appendChild(licensePlateCell);
        row.appendChild(vehicleTypeCell);
        row.appendChild(locationCell);
        row.appendChild(imageCell);

        // Add event listener for double-click on the license plate cell
        licensePlateCell.addEventListener('dblclick', () => {
            const editableInput = document.createElement('input');
            editableInput.type = 'text';
            editableInput.value = plate_number;
            editableInput.classList.add('editable-input');

            // Replace the license plate text with the editable input field
            licensePlateCell.innerHTML = '';
            licensePlateCell.appendChild(editableInput);
            editableInput.focus();

            // Add event listener to the editable input field
            editableInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    const newPlateNumber = editableInput.value.trim();
                    if (newPlateNumber !== plate_number) {
                        updateLicensePlateNumber(row, license_plate_id, newPlateNumber);
                    } else {
                        licensePlateCell.innerHTML = '';
                        licensePlateCell.appendChild(licensePlateText);
                    }
                }
            });

            editableInput.addEventListener('blur', () => {
                const newPlateNumber = editableInput.value.trim();
                if (newPlateNumber !== plate_number) {
                    updateLicensePlateNumber(row, license_plate_id, newPlateNumber);
                } else {
                    licensePlateCell.innerHTML = '';
                    licensePlateCell.appendChild(licensePlateText);
                }
            });
        });

        const insertIndex = rows.findIndex((row) => {
            const timeValue = new Date(row.cells[2].textContent).getTime();
            const resultTimeValue = new Date(time).getTime();

            return isTimeSortedAscending ? resultTimeValue < timeValue : resultTimeValue > timeValue;
        });

        if (insertIndex === -1) {
            trackTableBody.appendChild(row);
        } else {
            trackTableBody.insertBefore(row, rows[insertIndex]);
        }

        rows.push(row);
    });
}


function getVehicleType(plateNumber) {
    const lastTwoDigits = plateNumber.slice(-2);

    if (lastTwoDigits.startsWith('0')) {
        return 'private';
    } else if (lastTwoDigits.startsWith('1')) {
        return 'commercial';
    } else if (lastTwoDigits.startsWith('2')) {
        return 'public';
    } else if (lastTwoDigits.startsWith('4')) {
        return 'municipal';
    } else if (lastTwoDigits.startsWith('5')) {
        return 'government';
    } else {
        return 'unknown';
    }
}

function createDeviceEntry(deviceId) {
    const deviceList = document.getElementById('device-list');
    const deviceEntries = deviceList.getElementsByClassName('device-entry');

    const allDevicesIds = [];
    for (let i = 0; i < deviceEntries.length; i++) {
        const deviceIdSpan = deviceEntries[i].querySelector('.deviceId');
        if (deviceIdSpan) {
            const existingDeviceId = deviceIdSpan.textContent;
            allDevicesIds.push(existingDeviceId);
        }
    }

    if (!allDevicesIds.includes(deviceId)) {
        const entry = document.createElement('li');
        entry.classList.add('device-entry');
        entry.classList.add('normal');

        const deviceIdSpan = document.createElement('span');
        deviceIdSpan.textContent = deviceId;
        deviceIdSpan.classList.add('deviceId');

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.classList.add('delete-button');

        entry.appendChild(deviceIdSpan);
        entry.appendChild(deleteButton);

        // Add event listener to device entry
        deviceIdSpan.addEventListener('click', () => {
            const trackTableBody = document.getElementById('track-table-body');
            const licensePlateEntries = trackTableBody.getElementsByClassName('license-plate-entry');

            for (let i = 0; i < licensePlateEntries.length; i++) {
                const licensePlateEntry = licensePlateEntries[i];
                const licensePlateDeviceId = licensePlateEntry.querySelector('.deviceId').textContent;

                if (licensePlateDeviceId !== deviceId) {
                    if (licensePlateEntry.style.display === 'none') {
                        licensePlateEntry.style.display = '';
                    } else {
                        licensePlateEntry.style.display = 'none';
                    }
                } else {
                    licensePlateEntry.style.display = '';
                }
            }
        });

        deviceList.appendChild(entry);
    }
}

function updateLicensePlateNumber(row, license_plate_id, newPlateNumber) {
    const formData = new FormData();
    formData.append('id', license_plate_id);
    formData.append('plate_number', newPlateNumber);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`${updateLicensePlateUrl}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the license plate number in the table
            const licensePlateCell = row.querySelector('.license-plate-number');
            licensePlateCell.textContent = newPlateNumber;
        } else {
            console.error('License plate update failed:', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
  
function isValidLicensePlate(licensePlate) {
    const numberRegex = /^\d+$/;
    const licensePlateNumber = licensePlate.replace(/-/g, '');
    const licensePlateLength = licensePlateNumber.length;
    return (
        numberRegex.test(licensePlateNumber) &&
        (licensePlateLength === 4 || 
        (licensePlateLength === 7 && licensePlateNumber.slice(0,1) == '3'))
    );
}

function formatLicensePlate(licensePlate) {
    const licensePlateNumber = licensePlate.replace(/-/g, '');
    if (licensePlateNumber.length === 7) {
        return (
        licensePlateNumber.slice(0, 1) +
        '-' +
        licensePlateNumber.slice(1, 5) +
        '-' +
        licensePlateNumber.slice(5)
        );
    } else if (licensePlateNumber.length === 4) {
        return (
            '3-'+
        licensePlateNumber+
        '-**'
        );
    }
    return licensePlate;
}

function isDuplicateLicensePlate(licensePlate) {
    const licensePlates = Array.from(deviceList.getElementsByTagName('button'));
    const formattedLicensePlate = formatLicensePlate(licensePlate);
    return licensePlates.some((button) => button.textContent === formattedLicensePlate);
}

function handleLicensePlateClick(event) {
    const clickedLicensePlate = event.target;

    // Toggle active-only class for double-clicked license plate item
    if (clickedLicensePlate.classList.contains('active-only')) {
        clickedLicensePlate.classList.remove('active-only');
    } else {
        const activeOnlyItems = deviceList.getElementsByClassName('active-only');
        for (const item of activeOnlyItems) {
            item.classList.remove('active-only');
        }
        clickedLicensePlate.classList.add('active-only');
    }

    // Toggle normal/inactive class for all license plate items
    const licensePlateItems = deviceList.getElementsByTagName('li');
    for (const item of licensePlateItems) {
        if (item === clickedLicensePlate) {
            item.classList.toggle('normal');
            item.classList.remove('inactive');
        } else {
            item.classList.remove('normal');
            item.classList.add('inactive');
        }
    }
}

function handleLicensePlateDoubleClick(event) {
    const clickedLicensePlate = event.target.innerText;

    // Hide all entries in the track table
    const trackTableBody = document.getElementById('track-table-body');
    const trackTableEntries = trackTableBody.getElementsByTagName('tr');
    for (const entry of trackTableEntries) {
        entry.classList.add('hidden');
    }

    // Show only the entries with the selected license plate
    for (const entry of trackTableEntries) {
        const licensePlateCell = entry.getElementsByTagName('td')[3];
        if (licensePlateCell.innerText === clickedLicensePlate) {
            entry.classList.remove('hidden');
        }
    }
}

function handleTimeHeaderClick() {
    const trackTableBody = document.getElementById('track-table-body');
    const rows = Array.from(trackTableBody.getElementsByTagName('tr'));
  
    rows.sort((rowA, rowB) => {
      const timeA = new Date(rowA.cells[2].textContent);
      const timeB = new Date(rowB.cells[2].textContent);
  
      if (isTimeSortedAscending) {
        return timeA - timeB;
      } else {
        return timeB - timeA;
      }
    });
  
    isTimeSortedAscending = !isTimeSortedAscending;
    chevronDirection = isTimeSortedAscending ? '▼' : '▲';
    updateChevronDirection();
  
    trackTableBody.innerHTML = '';
  
    rows.forEach(row => trackTableBody.appendChild(row));
}

function updateChevronDirection() {
    const chevronElement = timeHeader.querySelector('.chevron');
    chevronElement.textContent = chevronDirection;
};

function addChevronToTimeHeader() {
    const chevronElement = document.createElement('span');
    chevronElement.classList.add('chevron');
    timeHeader.appendChild(chevronElement);
    updateChevronDirection();
}

function createRow() {
    const row = document.createElement('tr');
    row.classList.add('license-plate-entry');
    return row;
}

function createCell(content) {
    const cell = document.createElement('td');
    cell.textContent = content;
    return cell;
}

function createVehicleTypeCell(plate_number) {
    const vehicleTypeCell = document.createElement('td');
    const vehicleType = getVehicleType(plate_number);
    vehicleTypeCell.textContent = vehicleType;
    return vehicleTypeCell;
}

function createImageCell(imageData) {
    const imageCell = document.createElement('td');
    imageCell.classList.add('license-plate-image-cell');
    const licensePlateImage = document.createElement('img');
    licensePlateImage.src = 'data:image/jpeg;base64,' + imageData;
    licensePlateImage.classList.add('license-plate-image');
    imageCell.appendChild(licensePlateImage);
    return imageCell
}

function applyFilters() {
    const licensePlateInput = document.getElementById('track-input-field').value.trim();
    const startTimeInput = document.getElementById('start-time-input-field').value.trim();
    const endTimeInput = document.getElementById('end-time-input-field').value.trim();
    const vehicleTypeInput = document.getElementById('vehicle-type-input-field').value.trim();
    const locationInput = document.getElementById('location-input-field').value.trim();
    const deviceIdInput = document.getElementById('device-id-input-field').value.trim();
  
    const rows = Array.from(document.querySelectorAll('#track-table-body tr'));
  
    rows.forEach(row => {
      const licensePlateCell = row.querySelector('.license-plate-number');
      const timeCell = row.querySelector('td:nth-child(3)');
      const vehicleTypeCell = row.querySelector('td:nth-child(5)');
      const locationCell = row.querySelector('td:nth-child(6)');
      const deviceIdCell = row.querySelector('.deviceId');
  
      const licensePlate = licensePlateCell.textContent.trim();
      const time = new Date(timeCell.textContent.trim());
      const vehicleType = vehicleTypeCell.textContent.trim();
      const location = locationCell.textContent.trim();
      const deviceId = deviceIdCell.textContent.trim();
  
      const showRow =
        (licensePlateInput === '' || licensePlate.includes(licensePlateInput)) &&
        (startTimeInput === '' || time >= new Date(startTimeInput)) &&
        (endTimeInput === '' || time <= new Date(endTimeInput)) &&
        (vehicleTypeInput === '' || vehicleType.toLowerCase().includes(vehicleTypeInput.toLowerCase())) &&
        (locationInput === '' || location.toLowerCase().includes(locationInput.toLowerCase())) &&
        (deviceIdInput === '' || deviceId.includes(deviceIdInput));
  
      row.style.display = showRow ? '' : 'none';
    });
  }
  
function resetFilters() {
    const rows = Array.from(document.querySelectorAll('#track-table-body tr'));
    rows.forEach(row => {
        row.style.display = '';
    });
    document.getElementById('track-input-field').value = '';
    document.getElementById('start-time-input-field').value = '';
    document.getElementById('end-time-input-field').value = '';
    document.getElementById('vehicle-type-input-field').value = '';
    document.getElementById('location-input-field').value = '';
    document.getElementById('device-id-input-field').value = '';
}
// ----------------------------------------------------------------------------------------------------
//                                      utility functions
// ----------------------------------------------------------------------------------------------------

function createElement(tagName, attributes) {
    const element = document.createElement(tagName);
    if (attributes) {
        for (const key in attributes) {
            element.setAttribute(key, attributes[key]);
        }
    }
    return element;
}