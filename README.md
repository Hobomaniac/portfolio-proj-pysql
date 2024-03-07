# Running Logger

This project is meant for my portfolio project for class. It is incomplete and missing some functionality and probably should include a little more abstraction for the user end when adding data. So far you can only add data through json formats. This README.md is intended to get the project up and started, if you want to add data refer to the python files in the API directory in project/src.

## Requirements

* Docker and docker compose
* Insomnia (optional, mainly to GET/POST request)

## Installation

1. Clone the repository

2. In the root directory of the project (project/) run `docker compose up -d --build` 

3. Go to `http://localhost:5001/` and a hello world should appear in json format.

That's it, you should now be able to add/remove things from the database.
Again, check the api directory if you want to configure some json formats to GET/POST request to the database.
