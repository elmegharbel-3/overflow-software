import os
fbqn = "-b arduino:avr:nano "
sketch_1 = "~/overflow/one "
sketch_2 = "~/overflow/two "
port = "-p /dev/ttyUSB0 "
upload = "arduino-cli upload "
sketch_num = input("1 or 2 => ")
if sketch_num == "1":
    os.system(upload + fbqn + port + sketch_1)
elif sketch_num == "2":
    os.system(upload + fbqn + port + sketch_2)

