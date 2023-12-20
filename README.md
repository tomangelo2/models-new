models-new
==========

# New models for Colobot: Gold Edition
-----------
http://colobot.info ; https://github.com/colobot

Work repository for new models for Colobot: Gold Edition. They're compatible with upcoming new graphics engine.

# Installation
-----------
To see how new models look like in the game just copy the files placed in "gltf" directory to the "Colobot/Gold/Installation/Directory/data/models". The game should recognize new format and load new files instead of original ones.

If you want new models to be possible to turn on/off without moving files around you can also install them as a mod. Just make new directory in "UserProfileHomeDir\*/colobot/mods" directory (if it doesn't exist - create it) and name it as you wish, for example "HD-Models-Test-Mod". Inside your mod directory create "models" directory and copy there models you want to see in game. If you change your mind - simply delete/rename directory or files (renaming won't work with directory inside "mods").

No need to copy the other folders to the folder "data". Those files are not recognized by the game.

\* Depend of your Operating System:
**Windows**
Just type to your file explorer:
```
%UserProfile%\colobot
```

**Linux**
Just type to your file explorer:
```
$HOME
```

# Convenience submodules

## Convert models gltf->mod and vice versa

**ColobotModelConverter** is a converter made in [Godot Engine](https://godotengine.org/), which allows to easily convert existing models betwen gltf, mod and txt formats.
You only need to download a Godot binary and import this project. You don't even have to export it, just run it from the engine editor.

## Test all models in one level
-----------
**Alludo** is a level with every object available in game. It allows you to take a quick look at any model.
To install you need to either merge the *levels* directory with same directory inside *data* directory, or create a directory inside *mods* and paste the *levels* directory there.
