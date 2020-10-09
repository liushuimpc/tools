system/core/healthd/images/battery_scale.png

battery_scale.png -> battery00.png ~ battery05.png
	python interlace-frames.py -d battery_scale.png -o battery.png


battery00.png ~ battery05.png -> battery_scale.png
	python interlace-frames.py -o battery_scale.png oem/battery00.png oem/battery01.png oem/battery02.png oem/battery03.png oem/battery04.png oem/battery05.png