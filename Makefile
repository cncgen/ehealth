all: gui run

gui:
	pyuic4 ./app/gui.ui > ./app/gui.py

run:
	python ./app/main.py

clean:
	rm -r ./app/*.pyc
