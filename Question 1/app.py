from flask import Flask, request, jsonify
import requests
import json
import asyncio

app = Flask(__name__)

async def fetch_numbers(url):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=5)
        print(f"Response from {url}: {response.text}")
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except asyncio.TimeoutError:
        print(f"Timeout for URL: {url}")
    except Exception as e:
        print(f"Error fetching data from URL {url}: {e}")
    return []


@app.route('/numbers', methods=['GET'])
def get_merged_numbers():
    urls = request.args.getlist('url')
    tasks = [fetch_numbers(url) for url in urls]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    merged_numbers = list(set(number for sublist in results for number in sublist))
    merged_numbers.sort()

    return jsonify({"numbers": merged_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)