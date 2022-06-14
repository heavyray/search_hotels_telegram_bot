### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```
For Linux
```
$  virtualenv .
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Linux
```
$  source bin/activate
```

**3. Clone this project**
```
$  git clone https:https://github.com/heavyray/search_hotels_telegram_bot.git
```

Then, Enter the project
```
$  cd search_hotels_telegram_bot
```

**4. Install Requirements from 'requirements.txt'**
```python
$  pip3 install -r requirements.txt
```

**5. Install Requirements from 'requirements.txt'**

Command for Windows:
```python
$ python DB_services/set_db.py
```

Command for Linux:
```python
$ python3 DB_services/set_db.py
```

**6. Now Run Server**

Command for Windows:
```python
$ python main.py
```

Command for Linux:
```python
$ python3 main.py
```
