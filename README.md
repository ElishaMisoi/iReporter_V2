# iReporter_V2

[![Build Status](https://travis-ci.org/Elisha-Misoi/iReporter_V2.svg?branch=develop)](https://travis-ci.org/Elisha-Misoi/iReporter_V2) [![Coverage Status](https://coveralls.io/repos/github/Elisha-Misoi/iReporter_V2/badge.png?branch=develop)](https://coveralls.io/github/Elisha-Misoi/iReporter_V2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/24e20c83fead01ef634c/maintainability)](https://codeclimate.com/github/Elisha-Misoi/iReporter_V2/maintainability)

Corruption is a huge bane to Africa’s development. African countries must develop novel and localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.


## Features
1. Users can create an account and log in.
2. Users can create a ​ red-flag ​ record (An incident linked to corruption)
3. Users can create ​ intervention​​ record​ ​ (a call for a government agency to intervene e.g repair bad road sections, collapsed bridges, flooding e.t.c).
4. Users can edit their ​ red-flag ​ or ​ intervention ​ records.
5. Users can delete their ​ red-flag ​ or ​ intervention ​ records.
6. Users can add geolocation (Lat Long Coordinates) to their ​ red-flag ​ or ​ intervention records​ .
7. Users can change the geolocation (Lat Long Coordinates) attached to their ​ red-flag ​ or intervention ​ records​ .
8. Admin can change the ​ status​​ of a record to either ​ under investigation, rejected ​ (in the event of a false claim)​ ​ or​ resolved ( ​ in the event that the claim has been investigated and resolved)​

### Demo

Project API demo is hosted at [Heroku](https://ireporter-v2.herokuapp.com/)

### API endpoints

Prefix `/api/v2` to all api endpoints below

| **HTTP METHOD**   | **URI**  | **ACTION** |
|---|---|---|
|  **POST** |  `/auth/signup` | sign up a user |
|  **POST** |  `/auth/login` | login a user |
|  **POST** |  `/redflags` | post a red-flag |
|  **POST** |  `/interventions` | post an intervention |
|  **GET** |  `/redflags` | get list of all red-flags |
|  **GET** |  `/interventions` | get list of all interventions |
|  **GET** |  `/redflags/<int:redflag_id>` | get a red-flag record by `redflag_id` field |
|  **GET** |  `/interventions/<int:intervention_id>` | get an intervention record by `intervention_id` field |
|  **PATCH** |  `/redflags/<int:redflag_id>/location` | edit redflag location `redflag_id` field |
|  **PATCH** |  `/redflags/<int:redflag_id>/comment` | edit redflag redflag comment by `redflag_id` field |
|  **PATCH** |  `/redflags/<int:redflag_id>/status` | edit redflag record status by `redflag_id` field |
|  **PATCH** |  `/interventions/<int:intervention_id>/location` | edit intervention location `intervention_id` field |
|  **PATCH** |  `/redflags/<int:intervention_id>/comment` | edit redflag intervention comment by `intervention_id` field |
|  **PATCH** |  `/redflags/<int:intervention_id>/status` | edit redflag intervention status by `intervention_id` field |
| **DELETE**  |  `/redflags/<int:redflag_id>` | delete redflag record by `redflag_id` |
| **DELETE**  |  `/interventions/<int:intervention_id>` | delete intervention record by `intervention_id` |
|  **GET** |  `/users` | fetch all users |
|  **GET** |  `/users/<int:user_id>` | fetch one user by `user_id` |
|  **DELETE** |  `/users/<int:user_id>` | delete one user by `user_id` |


### Running the app locally
 - Clone the repo
 - `git clone https://github.com/Elisha-Misoi/iReporter_V2.git`

 - Create a virtual environment
 - `virtualenv venv`

 - Activate the virtual environment
 - `source venv/bin/activate`

 - Install dependencies
 - Navigate to the root of the application and run the command:
 - `pip install requirements.txt`

 - Create a database 
 - `sudo -u postgres psql`
 - `CREATE DATABASE ireporter;`
 
 - Activate database path
 - `source .env`

 - Run the app
 - `python run.py`



### Running Tests

 - Install nosetests
  `pip install nosetests`
  
 - Navigate to project root
 - Use `nosetests app/tests/` to run the tests
