#
# Makefile
.PHONY : all clean

PYUIC = pyside-uic

UIPYFILES := $(patsubst %.ui,%.py,$(wildcard *.ui))

all: table

table: $(UIPYFILES)

%.py: %.ui
	$(PYUIC) $< -o $@

clean:
	$(RM) *.pyc *_ui.py

