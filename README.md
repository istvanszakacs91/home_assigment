Macbook Flask app usage guide

# MySQL server install and populate user table
brew install mysql</br>
MySQL database without a root password. To secure it, run:</br>
mysql_secure_installation</br>

# Start MySQL server
mysql.server start</br>
mysql -u root -p</br>

# Setup Flask
virtualenv venv</br>
pip install -r requirements.txt</br>
## Run the app in terminal - option A
export FLASK_APP=my_app</br>
export FLASK_ENV=development</br>
flask run</br>
## Run the app in terminal - option B
python my_app.py