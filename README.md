# PirateGame - Angular Port

> This branch is currently under active development. The original releases of pirate game were built using completely vanilla JS, CSS and HTML. Having improved understanding and experience since the original release, we are now porting the application over to the javascript framework known as Angular.

### Setup
In order to install the necessary libraries on your machine, first clone the repo. Navigate to its directory and then src-ui and run:
```npm i```

The required libraries for the django application are located in ```python-requirements.txt``` and can be installed with ```pip install -r python-requirements.txt``.

### Usage
Simply run ```ng serve``` from within the src-ui directory to initiate the font-end server  
You must also run ```python django/pirategame/manage.py runserver``` to start the back-end API system

### Port Progress
| Status | Page | Notes |
|--------|------|-------|
🏗️|Index Page|missing counter for active games & patch notes for latest release|
✅|About Page||
✅|Tutorial page ||
🏗️| Patch notes | front-end complete but need notes loaded from server
❌| Create new game
❌| Join game | front page to enter GameID located at /play
❌| Sheet builder
❌| Lobby
❌| Gameplay
❌| Results
❌| Deployment scripts