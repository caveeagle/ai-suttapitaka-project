## Description

In this large project, I created a model for working with a database of Buddhist suttas.
The sutta texts are taken from an open source repository (**[SuttaCentral](https://github.com/suttacentral)**).

The model is based on a custom SQLite database and uses Google AI `gemini-2.5-pro`
to generate responses. To authenticate with Google AI and run the scripts, you must provide your own API key.

The model construction pipeline is described in the `PIPELINE.md` file.

The contents and structure of the Git directory are described in `FILES.md`.

To launch the GUI interface, run the `GUI-SUTTAPITAKA.py` file.

> **Note:** Without your personal API key, the model will not function.
