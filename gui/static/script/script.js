function setPrimaryCamera(element) {
    const middleContainer = document.getElementById("middle-container");

    // If the clicked element is already in the middle container
    if (middleContainer.contains(element)) {
        // Move it back to the original side container
        const originalContainer = element.dataset.originalParent;
        document.getElementById(originalContainer).appendChild(element);
        
        // Remove the original parent data attribute
        element.removeAttribute("data-original-parent");
    } else {
        // If there are already 2 items in the middle container
        if (middleContainer.children.length >= 2) {
            // Remove the first child (oldest camera)
            const oldestCamera = middleContainer.children[0];
            // Move it back to its original container
            const originalContainer = oldestCamera.dataset.originalParent;
            document.getElementById(originalContainer).appendChild(oldestCamera);
            // Remove the original parent data attribute
            oldestCamera.removeAttribute("data-original-parent");
        }

        // Move the clicked element to the middle container
        // Set the original parent container data attribute
        element.dataset.originalParent = element.parentNode.id; // Save the original parent ID
        middleContainer.appendChild(element);
    }
}
function changeQuality(element) {
    let camera = element.parentElement
    console.log(camera)
    let camera_index = camera.getAttribute("index")
    console.log("indwx from attribute",camera_index)
    let camera_quality = element.value
    console.log(camera_quality)
    let quality_url = `http://192.168.1.69:5000/video_feed/${camera_index}/quality`
    console.log(typeof data)
    fetch(quality_url,{
        method: "post",
        body: JSON.stringify({
            "index": camera_index,
            "quality": camera_quality
        }),
        headers: {
            "Content-type": "application/json"
        }
    })
}
function fetchJoystickStatus() {
    fetch('http://192.168.1.69:5001/joystick')  // Fetching from the data access server
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if(data.axes[3] != 0){
                displayData(data);
            }
        })
        .catch(error => {
            document.getElementById('output').innerHTML = `<p class="error">Error: ${error.message}</p>`;
        });
}

function displayData(data) {
    const output = document.getElementById('output');
    output.innerHTML = ''; // Clear previous output

    if (data.error) {
        output.innerHTML = `<p class="error">Error: ${data.error}</p>`;
    } else {
        console.log(data);
        output.innerHTML = `
            <h2>Joystick Name: ${data.name}</h2>
            <h3>Button States:</h3>
            <ul>
                ${Object.keys(data.buttons).map((buttonIndex) => {
                    const buttonState = data.buttons[buttonIndex];
                    return `<li>Button ${buttonIndex}: ${buttonState === 1 ? 'Pressed' : 'Not Pressed'}</li>`;
                }).join('')}
            </ul>
            <h3>Axis Positions:</h3>
            <ul>
                ${Object.keys(data.axes).map((axisIndex) => {
                    const axisValue = data.axes[axisIndex];
                    return `<li>Axis ${axisIndex}: ${axisValue.toFixed(2)}</li>`;
                }).join('')}
            </ul>
        `;
    }
}

// Fetch joystick status every x seconds
setInterval(fetchJoystickStatus, 100);


// Initial fetch when the page loads
fetchJoystickStatus();