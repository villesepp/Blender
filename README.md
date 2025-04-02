My Blender 3D scripts

# ⛰️ Terrain Generator
Simple procedural tool for making bumpy planes with options for customization. Developed in Blender 4.3.2.

### Install/Run
Open and run in the Blender Script Editor. A panel will appear in the 3D viewport ("N" menu on the right).

### Use
Click the Generate button and tweak the values using the box that appears on the bottom right.

### Key Features
- Adjustable size, height, subdivisions (level of detail), seed
- Two noise generators: Base and peak/valley
- Low limit for e.g. bodies of water
- Height-based vertex colors generation

### Download
[Take me to /terrain generator/](https://github.com/villesepp/Blender/tree/main/Terrain%20Generator)

### Screenshot
![alt text](https://github.com/villesepp/Blender/blob/main/readme%20images/terraingenerator.jpg "Screenshot")


# 📁 JSON export
Export some object properties to a JSON file. Useful if you want to use Blender as a Level Editor for your game and you are already using it for something else. Developed in Blender 4.3.2.

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

### Key Features
- Exports X, Y, Z coordinate (.1 precision)
- Exports Object's Custom Properties
- (ignores 'cycles' and 'booleans' properties that are enabled by default)

### Download
[Take me to /json export/](https://github.com/villesepp/Blender/tree/main/JSON%20export)

### Screenshot
![alt text](https://github.com/villesepp/Blender/blob/main/readme%20images/json.jpg "Screenshot")


