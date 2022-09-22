.PHONY: flask-i-run
# run flask server
flask-i-run:
		@python app.py

.PHONY: init-dev
# init requirements
init-dev:
		@python3 -m pip install --upgrade pip
		@pip install --requirement requirements.txt
