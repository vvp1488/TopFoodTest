<h1>Generate checks API Service</h1>
<ol>
  <li>create env</li>
  <li><b>pip install -r requirements.txt</b></li>
    <li><b>python3 manage.py makemigrations</b></li>
    <li><b>python3 manage.py migrate</b></li>
    <li><b>python3 manage.py loaddata fixtures/printer.json --app main.printer</b></li>
  <li>terminal 1: <b>docker-compose up</b></li>
  <li>terminal 2: <b>celery -A TopFood worker -l Info</b></li>
  <li>terminal 3: <b>python3 manage.py runserver</b></li>
</ol>

