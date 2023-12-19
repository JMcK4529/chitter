```
STRAIGHT UP

As a Maker
So that I can let people know what I am doing
I want to post a message (peep) to chitter

As a maker
So that I can see what others are saying
I want to see all peeps in reverse chronological order

As a Maker
So that I can better appreciate the context of a peep
I want to see the time at which it was made

As a Maker
So that I can post messages on Chitter as me
I want to sign up for Chitter
```
We need:
- tables: users, peeps // one user - to - many peeps
    - users has columns: id, username
    - peeps has columns: id, content, timestamp, user_id
- classes:
    - user = User(id, username, peeps=[])
        - #is_valid
        - #generate_errors
    - user_repo = UserRepository(connection)
        - #all
        - #find
        - #create
        - #delete
    - peep = Peep(id, content, timestamp, user_id)
        - #is_valid
        - #generate_errors
    - peep_repo = PeepRepository(connection)
        - #all
        - #find
        - #create
        - #delete
- routes: 
    - index: ('/')
        - should load all peeps in reverse order
        - should have some buttons:
            - sign up
            - log in
            - create peep - only show if logged in
        - pass in peeps (a list of Peep objects)
        - pass in users (a list of all User.username in id order)
    - sign up: ('/signup/')
        - should have a form to fill in to sign up (and submit button)
            - validate
            - if valid -> create User -> redirect to index page
            - if invalid -> return to /signup/ with errors
        - should have a link to go back to the index page
        - should have a link to go to the login page (I already have a Chitter account)
    - log in: ('/login/')
        - should have a form to fill in to log in (and submit button)
            - validate (i.e. user exists, password is correct)
            - if valid -> somehow store which user is logged in -> redirect to index page
            - if invalid -> return to /login/ with errors
        - should have a link to go back to index page
        - should have a link to go to the signup page (Sign Up?)
    - create peep: ('/new/')
        - should have a form to fill in to create peep (and submit button)
            - validate
            - if valid -> create Peep -> redirect to index page
            - if invalid -> return to /new/ with errors
        - should have a link to go back to index page
        - should have a link to go to the signup page (Sign Up?)
  
```
HARDER

As a Maker
So that only I can post messages on Chitter as me
I want to log in to Chitter

As a Maker
So that I can avoid others posting messages on Chitter as me
I want to log out of Chitter
```
  
```
ADVANCED

As a Maker
So that I can stay constantly tapped in to the shouty box of Chitter
I want to receive an email if I am tagged in a Peep
```
