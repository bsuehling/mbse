# mbse

### the python approach
Install requirements
```sh
pip install -r requirements.txt
```

Run the `main.py` script
```sh
python main.py
```

results will be generated in `artefacts`. `artefacts/io_automata` contains the io automata for each object. `artefacts/uml` contains the final UML2.0 state machines for each object. 

Diagrams are generated using [PlantUML](https://plantuml.com/).

> [!WARNING]  
> Requires active internet connection as we perform HTTP requests to the PlantUML server to generate the final diagrams.
