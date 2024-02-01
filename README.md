# Playground Reservation System

The Playground Reservation System is a web application built with Django, designed to facilitate the booking and management of playgrounds for players and owners.

## Preview

## Features

- **User Roles:**
  - Players can create accounts, view available playgrounds and slots, and book playgrounds.
  - Playground owners can add playgrounds, manage available slots, and accept or reject booking requests.

- **Playground Management:**
  - Playground owners can add playgrounds, set capacities, and specify the type of grass (artificial or natural).

- **Slot Booking:**
  - Users can book available slots in playgrounds, and owners can manage slot bookings.

## Setup Instructions

- Clone this repo
``` shell
git clone https://github.com/your/your-project.git
```
<br>

- Install project dependencies
```shell
pip install -r requirements.txt
```
<br>

- Open the project folder with any IDE
- Run these commands
``` shell
python3 manage.py make migrations
python3 manage.py migrate
```
<br>

- Run the development server
```shell
python3 manage.py runserver
```
