let joystick = document.getElementById("joystick");
console.log("hello");
function fetch_joy() {
  while (true) {
    let joy_data = fetch_joy("/joystick");
    console.log(joy_data);
    joystick.innerHTML(joy_data);
  }
}
