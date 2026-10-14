# LAST STAND — Zombie Survival

Browser-playable survival game embedded in a Streamlit app.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open the local URL shown in the terminal, usually http://localhost:8501.

## Controls
- Move: WASD or arrow keys
- Aim: mouse
- Shoot: left mouse button or Space
- Collect supplies: E near a crate
- Pause/resume: Escape or Pause button
- Restart: Restart button

## Publish with GitHub + Streamlit Community Cloud
1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Choose Create app, select your repository, branch `main`, and main file `app.py`.
4. Click Deploy and share the generated `*.streamlit.app` URL.

The game runs in an HTML Canvas embedded component, so the hosted app does not need Pygame installed.
