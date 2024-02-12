.PHONY: install
install:
	#python3 setup.py install
	pip3 install .

.PHONY: package
package:
	python3 setup.py sdist bdist_wheel

# Setup to create a single .exe for distribution
.PHONY: executable
executable:
	pyinstaller --clean --windowed --specpath "./build" --upx-dir "./build"  --icon "../lcapygui/data/icon/lcapy-gui.png" --add-data "../lcapygui/data/:lcapygui/data/" --hidden-import='PIL._tkinter_finder' lcapygui.py

.PHONY: upload-test
upload-test: package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: package
	python3 -m twine upload dist/*

.PHONY: test
test: lcapy-gui/*.py
	nosetests -s --pdb

.PHONY: cover
cover: lcapy-gui/*.py
	nosetests --pdb --with-coverage --cover-package=lcapy-gui --cover-html

.PHONY: doc
release: doc push
	cd /tmp; rm -rf lcapy-gui; git clone git@github.com:mph-/lcapy-gui.git; cd lcapy-gui; make test; make upload

.PHONY: release-test
release-test: doc push
	cd /tmp; rm -rf lcapy-gui; git clone git@github.com:mph-/lcapy-gui.git; cd lcapy-gui; make test

.PHONY: style-check
style-check:
	flake8 lcapy-gui
	flake8 doc

.PHONY: flake8
flake8:
	flake8 lcapy-gui
	flake8 doc

.PHONY: check
check: style-check

.PHONY: push
push: check
	git push
	git push --tags

.PHONY: doc
doc:
	cd doc; make html

.PHONY: clean
clean:
	-rm -rf build lcapy-gui.egg-info dist
	cd doc; make clean
