// ------------------------------ navbar functionality ----------------------------------------

let activeTab = "about";
document.addEventListener("DOMContentLoaded", initializeTabs);

// ------------------------------ dashboard tab functionality ----------------------------------------

const addDeviceBtn = document.getElementById('add-device-btn');
const closePopupButton = document.getElementById('close-popup-button');
const deviceTypeSelect = document.getElementById('device-type');
const confirmDeviceBtn = document.getElementById('confirm-device-btn');


addDeviceBtn.addEventListener('click', showPopupWindow);
closePopupButton.addEventListener('click', hidePopupWindow);
deviceTypeSelect.addEventListener('change',  configurePopupInputFields);
confirmDeviceBtn.addEventListener('click',  handleNewDevice);


// ------------------------------ tracking tab functionality ----------------------------------------

const trackBtn = document.getElementById('track-btn');
const licensePlateList = document.getElementById('license-plate-list');

trackBtn.addEventListener('click', handleTrackFunction);
licensePlateList.addEventListener('click', handleLicensePlateClick);
licensePlateList.addEventListener('dblclick', handleLicensePlateDoubleClick);

// instead of the method below, why not just add an X button?
// licensePlateList.addEventListener('mousedown', handleLicensePlateSlide);
// licensePlateItem.addEventListener('mousemove', handleMouseMove);
// licensePlateItem.addEventListener('mouseup', handleMouseUp);
// licensePlateItem.addEventListener('mouseleave', handleMouseLeave);


// ----------------------------------------------------------------------------------------------------
//                                      navbar functions
// ----------------------------------------------------------------------------------------------------

const dashboardSideNav = document.querySelector('.dashboard_sidenav');
const trackSideNav = document.querySelector('.track_sidenav');


function initializeTabs() {
    const tabLinks = document.getElementsByClassName("topnav")[0].getElementsByTagName("a");

    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].addEventListener("click", handleTabClick);
    }

    showContent(activeTab);
    toggleSideNavContent(activeTab);
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
        dashboardSideNav.style.display = 'flex';
        trackSideNav.style.display = 'none';
    } else if (activeTab === 'track') {
        dashboardSideNav.style.display = 'none';
        trackSideNav.style.display = 'flex';
    }
}


// ----------------------------------------------------------------------------------------------------
//                                      dashboard functions
// ----------------------------------------------------------------------------------------------------

const addDevicePopup = document.getElementById('add-device-popup');

function showPopupWindow() {
    addDevicePopup.style.display = 'block';
}

function hidePopupWindow() {
    addDevicePopup.style.display = 'block';
}

function configurePopupInputFields() {
    const selectedType = deviceTypeSelect.value;
    const fileInput = document.getElementById('file');
    const recordingTimeInput = document.getElementById('recording-time');

    fileInput.required = selectedType === 'video' || selectedType === 'image';

    recordingTimeInput.required = selectedType !== 'camera';

    if (selectedType === 'camera') {
        recordingTimeInput.value = getCurrentTime();
    } else {
        recordingTimeInput.value = '';
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

    const deviceType = deviceTypeSelect.value;
    const deviceId = document.getElementById('device-id').value;
    const deviceName = document.getElementById('device-name').value;
    const recordingTime = document.getElementById('recording-time').value;
    const deviceLocation = document.getElementById('device-location').value;
    const fileInput = document.getElementById('file');
    const devicesList = document.querySelector('.dashboard_sidenav_inner_1 .devices');
    const file = fileInput.files[0];

    if (deviceType === '' || deviceId === '' || deviceName === '') {
        alert('Error: Please fill in all required fields.');
        return;
    }

    // Add the device to the list
    const deviceLinkText = `${deviceName}`;
    const deviceLink = createElement('a', { href: '#', class: 'device-link' });
    deviceLink.textContent = deviceLinkText;
    const deviceListItem = createElement('li', { class: 'device' });
    deviceListItem.appendChild(deviceLink);
    const deviceIdParagraph = createElement('p', { class: 'device-id' });
    deviceIdParagraph.textContent = `${deviceType.charAt(0).toUpperCase()}${deviceType.slice(1)} - ${deviceId}`;
    deviceListItem.appendChild(deviceIdParagraph);
    devicesList.appendChild(deviceListItem);

    const popup = document.getElementById('add-device-popup');
    popup.style.display = 'none';

    const formData = new FormData();
    formData.append('deviceType', deviceType);
    formData.append('deviceId', deviceId);
    formData.append('deviceName', deviceName);
    formData.append('recordingTime', recordingTime);
    formData.append('deviceLocation', deviceLocation);
    formData.append('file', file);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`${ uploadFileUrl }`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        refreshResults(data.results);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function refreshResults(results) {
    const tableBody = document.getElementById('table-body');

    // Get the current number of table rows
    const rowCount = tableBody.rows.length;

    // Iterate over the results and add entries to the table in reverse order
    for (let i = results.length - 1; i >= 0; i--) {
        const frameResults = results[i];
        frameResults.forEach((result, index) => {
            const {
                plate_number,
                confidence_score,
                image_data,
                time,
                device_identifier,
                device_type,
                location,
            } = result;

            // Create a new table row
            const row = document.createElement('tr');

            // Create table cells for each data field
            const entryCell = document.createElement('td');
            entryCell.textContent = rowCount + index + 1;
            row.appendChild(entryCell);

            const deviceIdCell = document.createElement('td');
            deviceIdCell.textContent = device_identifier;
            row.appendChild(deviceIdCell);

            const timeCell = document.createElement('td');
            timeCell.textContent = time;
            row.appendChild(timeCell);

            const licensePlateCell = document.createElement('td');
            licensePlateCell.textContent = plate_number;
            row.appendChild(licensePlateCell);

            const locationCell = document.createElement('td');
            locationCell.textContent = location;
            row.appendChild(locationCell);

            // Insert the new row at the beginning of the table body
            tableBody.insertBefore(row, tableBody.firstChild);
        });
    }
}


// ----------------------------------------------------------------------------------------------------
//                                      track functions
// ----------------------------------------------------------------------------------------------------

const trackInputField = document.getElementById('track-input-field');

function handleTrackFunction(event) {
    event.preventDefault();
    const licensePlate = trackInputField.value;
    if (isValidLicensePlate(licensePlate) && !isDuplicateLicensePlate(licensePlate)) {
        const formattedLicensePlate = formatLicensePlate(licensePlate); // 3-dddd-dd or 3-dddd-**

        const licensePlateItem = document.createElement('li');
        licensePlateItem.innerText = formattedLicensePlate;
        licensePlateItem.classList.add('normal');
        licensePlateItem.classList.add('license-plate');
        licensePlateItem.innerText = formattedLicensePlate;
        licensePlateList.appendChild(licensePlateItem);

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        const url = `${ searchByPlateUrl }?licensePlate=${encodeURIComponent(formattedLicensePlate)}`;
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(results => {
            appendResultsToTrackTable(results);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        trackInputField.value = '';
    } else {
        alert('Invalid plate\nLicense Plate must be either a 4- or a 7-Digit unique number\nIf it\'s a 7-Digit number, then it must start with 3');
    }
}

function appendResultsToTrackTable(results) {
    const trackTableBody = document.getElementById('track-table-body');

    results.forEach((result, index) => {
        const {
            plate_number,
            confidence_score,
            image_data,
            time,
            device_identifier,
            device_type,
            location,
        } = result;

        const row = document.createElement('tr');

        const entryCell = document.createElement('td');
        entryCell.textContent = index + 1;
        row.appendChild(entryCell);

        const deviceIdCell = document.createElement('td');
        deviceIdCell.textContent = device_identifier;
        row.appendChild(deviceIdCell);

        const timeCell = document.createElement('td');
        const formattedTime = new Date(time).toLocaleString();
        timeCell.textContent = formattedTime;
        row.appendChild(timeCell);

        const licensePlateCell = document.createElement('td');
        licensePlateCell.textContent = plate_number;
        row.appendChild(licensePlateCell);

        const locationCell = document.createElement('td');
        locationCell.textContent = location;
        row.appendChild(locationCell);

        trackTableBody.appendChild(row);
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
    const licensePlates = Array.from(licensePlateList.getElementsByTagName('button'));
    const formattedLicensePlate = formatLicensePlate(licensePlate);
    return licensePlates.some((button) => button.textContent === formattedLicensePlate);
}

function handleLicensePlateClick(event) {
    const clickedLicensePlate = event.target;

    // Toggle active-only class for double-clicked license plate item
    if (clickedLicensePlate.classList.contains('active-only')) {
        clickedLicensePlate.classList.remove('active-only');
    } else {
        const activeOnlyItems = licensePlateList.getElementsByClassName('active-only');
        for (const item of activeOnlyItems) {
            item.classList.remove('active-only');
        }
        clickedLicensePlate.classList.add('active-only');
    }

    // Toggle normal/inactive class for all license plate items
    const licensePlateItems = licensePlateList.getElementsByTagName('li');
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

function handleLicensePlateSlide(event) {
    const licensePlateItem = event.target;
    const startX = event.pageX;
}

function handleMouseMove(e) {
    const x = e.pageX;
    const diff = x - startX;

    if (Math.abs(diff) > 50) {
        licensePlateItem.removeEventListener('mouseup', handleMouseUp);
        licensePlateItem.removeEventListener('mouseleave', handleMouseLeave);

        // Prompt confirmation window
        const confirmed = confirm('Are you sure you want to delete this license plate?');

        if (confirmed) {
            // Delete the license plate and its corresponding entries
            licensePlateList.removeChild(licensePlateItem);
            const licensePlate = licensePlateItem.innerText;

            const trackTableBody = document.getElementById('track-table-body');
            const trackTableEntries = trackTableBody.getElementsByTagName('tr');
            for (const entry of trackTableEntries) {
                const licensePlateCell = entry.getElementsByTagName('td')[3];
                if (licensePlateCell.innerText === licensePlate) {
                    trackTableBody.removeChild(entry);
                }
            }
        }
    }
}

function handleMouseUp() {
    licensePlateItem.removeEventListener('mousemove', handleMouseMove);
}

function handleMouseLeave() {
    licensePlateItem.removeEventListener('mousemove', handleMouseMove);
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