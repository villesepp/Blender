My Blender 3D scripts

# ⛰️ Terrain Generator
Simple procedural tool for making bumpy planes with options for customization.

### Install/Run
Open and run in the Blender Script Editor. A panel will appear in the 3D viewport ("N" menu on the right).

### Use
Click the Generate Procedural Terrain button and tweak the values using the box that appears on the bottom right.

## Features
- Plane size
- Subdivisions (cuts)
- Noise Scale
- Height Multiplier
- Seed offset
- Height-based bertex colors
- Smooth shading on/off

### Screenshot
![alt text](https://github.com/villesepp/Blender/blob/main/readme%20images/terraingenerator.jpg "Screenshot")


# 📁 JSON export
Export some object properties to a JSON file. Useful if you want to use Blender as a Level Editor for your game and you are already using it for something else.

### Install/Run
Open and run in the Blender Script Editor.

### Use
It will export everything in the current collection and the collection itself. There is currently no UI yet, due to the lack of a need for it. A JSON file with the same name as the collection will be generated in the same folder as the blender project file.

### Usage example case as a level editor tool
- Create a collection "level_01"
- Add some objects, such as terrain pieces, with proper names like "ground" or "water"
- Add custom properties to e.g. a "water" object, like depth: 5, for deep water
- Run the script to get a file "level_01.json"
- Read the file in your game engine and generate the level graphics using the coordinates from the JSON file

## Exports
- X, Y, Z coordinate (.1 precision)
- Object's Custom Properties
- (ignores 'cycles' and 'booleans' properties that are enabled by default)

### Screenshot
![alt text](https://github.com/villesepp/Blender/blob/main/readme%20images/json.jpg "Screenshot")


