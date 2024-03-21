# dj-book-rental

Live Application: http://34.224.38.214/  which allows students to rent books. Although this project is built as an asssement, the following documentation provides context to the problem.

## Running Application

To run application locally, ensure to have [make](https://leangaurav.medium.com/how-to-setup-install-gnu-make-on-windows-324480f1da69), [docker](https://docs.docker.com/engine/install/), and [docker compose](https://docs.docker.com/compose/install/) installed. The application is managed with poetry python package and environment manager.

**STEPS**

- clone the repository to your local machine from github

- navigate into the cloned folder

- create a `.env` file 

- fill all environment variables contained in `env.example` within `.env` by replacing all `xxxx` with their appropriate values

- Open up your terminal and ensure to navigate to the cloned folder

- Run `make build` - this would build the application docker image with all necessary dependencies as contained in pyproject.toml file

- Run `make serve` - this would start the application using the built docker image and also all services it is dependent on

- Open your browser and vist `http://localhost` which would present the landing page the application

- You can also view application logs by running `make logs`


## The Problem

The solution provided by this platform is ease in book rental. This allows librarian to rent out books to student or registered member of the library.

The system currently caters for:

### Available Features

- Realtime validation when interacting with forms using **HTMX**

- A librarian can add a student to the platform

- A librarian can rent out book to a student

- A librarian can extend book return date on behalf of student for a given rental

- Authentication system to allow access to librarian to the rental system

- Registration flow to allow a librarian to register if they don't have an account 

- Utilizes OpenLibrary API for book search

- A librarian can unauthenticate


## Application Structure

The platform contains a single application called rentals within which is contained the application

- models (`models.py`): Contains class based representation of the database table for each Entity e.g Student, Book, etc

- views (`views.py`): Contains controller wherein the business logic of the application is managed

- urls (`urls.py`): A route table for the application which maps request path to controllers

- forms (`forms.py`): Contains form object to facilitate collection of data from the client




