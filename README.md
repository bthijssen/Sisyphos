# Sisyphos
## .ENV
Make sure to make a _.env_ file based on the _.env.example_ file

### CHROME_WEBDRIVER_PATH
Get chromedriver from https://googlechromelabs.github.io/chrome-for-testing/#stable and set the CHROME_WEBDRIVER_PATH to the path of this file.

### URL
The url for the resale platform of the 4Daagse. In 2025 this was https://atleta.cc/e/zRLhtOq7pOcB/resale?initialUrl=https%3A%2F%2Fwww.4daagse.nl%2F&finalUrl=https%3A%2F%2Fwww.4daagse.nl%2F

### PUSH_API_TOKEN, PUSH_USER_KEY, PUSH_URL
Values from [Pushover](https://pushover.net/)

## How to run
Have _uv_ installed (for example with `brew install uv`)

Run with
```bash
uv run sisyphus
```


