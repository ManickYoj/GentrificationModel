# GentrificationModel
An Markov-Chain, Monte-Carlo model of gentrification for Olin's Discrete Math class in Fall 2016

# Installation
```
git clone https://github.com/ManickYoj/GentrificationModel.git
cd GentrificationModel
pip install -r requirements.txt
```

# API Key Setup
Note: Setting up API keys is required to modify the basic data underlying the model, but not to run the model.

API keys for this model are stored in a private file named `private.json`. To not spread API keys around, that file is included in the gitignore so that keys aren't publicly published. To setup your keys, copy the following code into a file in the root directory name `private.json` and fill in your API keys where they are called for.

`private.json`:
```
{
    "API-keys": {
        "census": "Your Key Here"
    }
}
```