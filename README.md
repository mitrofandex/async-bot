## How to run this bot

1. Create your application (https://core.telegram.org/api/obtaining_api_id) and bot (@BotFather)
2. Add your `config.py` with your `api_id`, `api_hash` and bot `token`
```python
token = '12345:abcde'
api_id = 123456
api_hash = 'abcde12345'
```
3. Run `docker build -t pyrobot .` from project directory
4. Run `docker run -d --rm  pyrobot`