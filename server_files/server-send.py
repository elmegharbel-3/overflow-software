import flask
import pygame
import json

pygame.init()
pygame.joystick.init()
my_joy = pygame.joystick.Joystick(0)
my_joy.init()
app = flask.Flask(__name__)
latest_data = None
@app.route('/joystick', methods=["GET"])
def index():
    pygame.event.pump()
    axis_data = [my_joy.get_axis(j) for j in range(my_joy.get_numaxes())]
    button_data = [my_joy.get_button(j) for j in range(my_joy.get_numbuttons())]
    j_data = {
        "axis": axis_data,
        "buttons": button_data
    }
    print(j_data)
    return json.dumps(j_data)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080,threaded=False)
    