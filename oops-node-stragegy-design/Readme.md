# Strategy Design pattern

- Makes the whole code act as lego blocks
- You can swap and switch each blocks to suit your needs
- Here I can have two type of database, either an Inmemeory db or a redis db
- can toggle between then using a config env
- now all this class and stuff makes a bit of sense
    - I don't have to change the route logic if I change the db
    - can i package all the utils or checks or any other things i want in my class
    - constructer is like a startup script where you can run certains self checks or other thing that needes to be executed once on startup aka when the class is being initiated.