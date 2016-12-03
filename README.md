# GentrificationModel
An agent-based + cellular automata model of gentrification for Olin's Discrete Math class in Fall 2016

# API Key Setup
Note: Setting up API keys is required to modify the basic data underlying the model, but not to run the model.

API keys for this model are stored in a private file named `private.json`. Evidently, that file is included in the gitignore so that keys aren't publicly published. To setup your keys, copy the following code into a file in the root directory name `private.json` and fill in your API keys where they are called for.

`private.json`:
```
{
    "API-keys": {
        "census": "Your Key Here"
    }
}
```