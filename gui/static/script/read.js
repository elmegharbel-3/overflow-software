import data from "./../json/camera_data.json" with { type: "json" };
console.log(data);
let quality_select = document.querySelectorAll("select")
console.log(quality_select)
function setQuality() {
    for (let i = 0;i < quality_select.length;i++) {
        let index = quality_select[i].getAttribute("index")
        let value = data[index]
        let options = quality_select[i].querySelectorAll("option")
        for (let i = 0;i < options.length;i++) {
            if (options[i].value == value) {
                options[i].selected = "selected"
            }
        }
    }
}
setQuality()

