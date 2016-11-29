SwiftSwap

SwiftSwap overcomes the biggest challenge with bartering and that its hard to find what you want from the person who will barter for the skill you have.

SwiftSwap searches the user network to find a closed path⭕ between users which means every user gets access to the skill they want without a one to one exchange.

It utilizes a NetworkX method of finding elementary circuits based on Johnson's algorithm called simple_cycles. It locates a closed loop where the beginning and ending of the path is the same user⭕.

Users can sign up, enter their wanted and offered skills and find out if there is a closed path⭕ in the network that makes their bartering experience swift. Users also have access to users in their closed path⭕, can view their location and graphical representation of their path. 
The first degree connections graph shows users their network neighbors - direct connections to the user. 

SwiftSwap Homepage

![SwiftSwap Homepage](assets/ss1.png)

## Table of Contents📖

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [Demo](#demo)
* [To-Do](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ D3, Chart.js, Jinja2, Javascript, jQuery, Bootstrap <br/>
__Backend:__ Python, NetworkX, Flask, PostgreSQL, SQLAlchemy, bcrypt, faker, pandas, NumPy, scikit-learn, geocoder <br/>
__APIs:__ Google Maps API <br/>

## <a name="features"></a>Features

Homepage D3 network graph with user nodes and skill edges

![SwiftSwap Homepage](assets/ss2.png)

Pagerank of the most popular users and Chart.js doughnut visualization

![SwiftSwap Homepage](assets/ss3.png)

User profile page with current and predicted skills

![SwiftSwap Homepage](assets/ss4.png)

User closed path⭕ D3 graph and first degree connections D3 graph

![SwiftSwap Homepage](assets/ss5.png)

User closed path⭕ connections links and user location map

![SwiftSwap Homepage](assets/ss6.png)

## <a name="installation"></a>Setup/Installation

####Requirements:

- PostgreSQL
- Python 2.7
- Google Maps API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/skakanka/swiftswap.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own Google Maps API key and save it to a file `secrets.py`.
```
Create database 'barternet'.
```
$ createdb -E UTF8 -T template0 --locale=en_US.utf8 barternet
```
Create your database tables and seed example data.
```
$ python barter_network/seed.py
```
Run the app from the command line.
```
$ python runserver.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

## <a name="demo"></a>Demo

![SwiftSwap Demo](assets/swiftswap_demo.gif)

## <a name="future"></a>TODO
* Map users within the shortest distance of each other in the closed path⭕
* User reviews, verification and photos
* Add ability for users to communicate
* Develop system for valuing skills


## <a name="license"></a>License

The MIT License (MIT)
Copyright (c) 2016 Anka Kondraska 

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.