# Dropbox Dataset Builder
> A simple application that generates image data sets for training neural networks.

## Getting Started
Given a search query, the application will scrape Google for images and upload them to a designated dropbox folder.
1. Run 'python3 dropbox_app.py' in the terminal
2. Generate an authorization token following the steps provided in the CLI.
3. Enter your authorization token.
4. Enter the name of the dropbox destination folder.
5. Enter a search query.

### Requirements
1. Python3
2. dropbox python library
```
pip3 install dropbox
```
3. selenium python library
```
pip3 install selenium
```
4. json python library
```
pip3 install json
```
