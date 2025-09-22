# Python API Requests Lab Guide

### Prerequisites:
1. **Verify Installation**  

   ```bash
   # Check Python version
   python --version
   
   # Check pip version
   python -m pip --version
   ```

2. **Create and Activate Virtual Environment**  
   
   1. Open **Visual Studio Code**.
   2. Click **File > Open Folder**.
   3. Choose a location and click **New Folder**.
   4. Name the folder `python-api-lab` and click **Open**.
   5. In VS Code, press `Ctrl + Shift + P` (**Command Palette**).
   6. Type `Python: Create Environment`, select it.
   7. Choose `Venv`.
   8. Select `Use Current Workspace Folder`.
   9. A `.venv` folder appears when finished.
   10. Right click the `.venv` folder and click **Open in Integrated Terminal**

**Install Required Packages**  

**Note: Always make sure your virtual environment is activated (you'll see `(venv)` in your prompt) when installing packages or running your code.**

### How to Run Any Example in this Guide

1. **Make sure your virtual environment is activated**

   ```bash
   # You should see (venv) at the start of your prompt
   # If not, activate it:
   Scripts\activate
   ```
 
2. In the new terminal type: 

   ```bash
   # After activating virtual environment
   python -m pip install requests aiohttp
   ```

   
3. **Create a Python file**
   
   1. Make sure you are in the `.venv` folder and create a new file. You can name it whatever you want (e.g `get.py`)
   
4. **Copy the example code (from below)** into your .py file

5. **Run the code**
   
   ```bash
   python example.py
   ```

Note: These steps apply to ALL code examples in this guide. Just copy any example into a .py file and run it using `python filename.py`

### Step 1: Basic GET Request
Let's start with a simple GET request to retrieve data from an API.

```python
import requests

# Make a GET request to a public API
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
```

### Step 2: Making POST Requests
Create new resources using POST requests.

```python
import requests

# Data to send in the POST request
new_post = {
    'title': 'My New Post',
    'body': 'This is the content of my post',
    'userId': 1
}

# Make a POST request
response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=new_post
)

# Check response
if response.status_code == 201:
    created_post = response.json()
    print("Created post:", created_post)
else:
    print(f"Error: {response.status_code}")
```

### Step 3: Adding Headers
Learn how to add custom headers to your requests.

```python
import requests

# Define headers
headers = {
    'User-Agent': 'Python API Lab Client',
    'Accept': 'application/json'
}

# Make request with headers
response = requests.get(
    'https://jsonplaceholder.typicode.com/posts/1',
    headers=headers
)

print(f"Status Code: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Data: {response.json()}")
```

### Step 4: Handling Query Parameters
Add query parameters to your requests for filtering and pagination.

```python
import requests

# Parameters as a dictionary
params = {
    'page': 1,
    'limit': 10,
    'sort': 'desc'
}

# Make GET request with parameters
response = requests.get(
    'https://jsonplaceholder.typicode.com/posts',
    params=params
)

# URL with parameters will be printed
print(f"Request URL: {response.url}")
print(f"Results: {response.json()[:2]}")  # Print first 2 results
```

### Step 5: PUT and PATCH Requests
Update existing resources using PUT and PATCH.

```python
import requests

# PUT request (full update)
put_data = {
    'id': 1,
    'title': 'Updated Title',
    'body': 'Updated body content',
    'userId': 1
}

put_response = requests.put(
    'https://jsonplaceholder.typicode.com/posts/1',
    json=put_data
)

print("PUT Response:")
print(f"Status Code: {put_response.status_code}")
print(f"Updated Data: {put_response.json()}\n")

# PATCH request (partial update)
patch_data = {
    'title': 'Only Update Title'
}

patch_response = requests.patch(
    'https://jsonplaceholder.typicode.com/posts/1',
    json=patch_data
)

print("PATCH Response:")
print(f"Status Code: {patch_response.status_code}")
print(f"Updated Data: {patch_response.json()}")
```

### Step 6: DELETE Requests
Remove resources using DELETE requests.

```python
import requests

# Make DELETE request
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')

# Check if deletion was successful
if response.status_code == 200:
    print("Resource deleted successfully")
else:
    print(f"Error deleting resource: {response.status_code}")
```

### Step 7: Error Handling
Implement proper error handling for your API requests.

```python
import requests
from requests.exceptions import RequestException

def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting to server: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    
    return None

# Test with valid URL
print("\nTesting valid URL:")
result = make_api_request('https://jsonplaceholder.typicode.com/posts/1')
if result:
    print("Success! Retrieved data:", result)
else:
    print("Failed to retrieve data")

# Test with 404 error
print("\nTesting 404 error:")
result = make_api_request('https://jsonplaceholder.typicode.com/posts/999')
if result:
    print("Success! Retrieved data:", result)
else:
    print("Failed as expected - resource not found")

# Test with invalid URL
print("\nTesting invalid URL:")
result = make_api_request('https://invalid-url-that-does-not-exists.com')
if result:
    print("Success! Retrieved data:", result)
else:
    print("Failed as expected - invalid URL")
```

### Step 8: Working with Sessions
Use sessions to maintain cookies and connection pools.

```python
import requests

# Create a session
session = requests.Session()

# Set default headers for all requests in this session
session.headers.update({
    'User-Agent': 'Python API Lab Client',
    'Accept': 'application/json'
})

# Make multiple requests using the session
response1 = session.get('https://jsonplaceholder.typicode.com/posts/1')
response2 = session.get('https://jsonplaceholder.typicode.com/posts/2')

# Print results
print("First request:")
print(f"Status Code: {response1.status_code}")
print(f"Data: {response1.json()}\n")

print("Second request:")
print(f"Status Code: {response2.status_code}")
print(f"Data: {response2.json()}")

# Close the session when done
session.close()
```

### Step 9: Testing Authentication with Postman and Python
Learn how to test different authentication methods using both Postman and Python.

#### Basic Authentication
**Postman:**
Install Postman from [here](https://dl.pstmn.io/download/latest/win64)

1. Create a new request to `https://httpbin.org/basic-auth/user/pass`
2. Under the "Authorization" tab, select "Basic Auth"
3. Enter:
   - Username: `user`
   - Password: `pass`

**Python equivalent:**
```python
import requests

# Basic Authentication
response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=('user', 'pass')
)
print("Basic Auth Response:", response.json())
```

#### Bearer Token
**Postman:**
1. Create a new request to `https://httpbin.org/bearer`
2. Under the "Authorization" tab, select "Bearer Token"
3. Enter token: `my-test-token`

**Python equivalent:**
```python
import requests

# Bearer Token Authentication
headers = {
    'Authorization': 'Bearer my-test-token'
}
response = requests.get(
    'https://httpbin.org/bearer',
    headers=headers
)
print("Bearer Token Response:", response.json())
```

#### API Key
**Postman:**
1. Create a new request to `https://httpbin.org/headers`
2. Under the "Headers" tab, add:
   - Key: `X-API-Key`
   - Value: `my-api-key-123`

**Python equivalent:**
```python
import requests

# API Key in Headers
headers = {
    'X-API-Key': 'my-api-key-123'
}
response = requests.get(
    'https://httpbin.org/headers',
    headers=headers
)
print("Headers Response:", response.json())
```

#### Complete Testing Script
```python
import requests

def test_auth_methods():
    print("\n=== Testing Different Auth Methods ===\n")

    # Test Basic Auth
    try:
        response = requests.get(
            'https://httpbin.org/basic-auth/user/pass',
            auth=('user', 'pass')
        )
        print("Basic Auth Test:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"Basic Auth Error: {e}\n")

    # Test Bearer Token
    try:
        headers = {'Authorization': 'Bearer my-test-token'}
        response = requests.get(
            'https://httpbin.org/bearer',
            headers=headers
        )
        print("Bearer Token Test:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"Bearer Token Error: {e}\n")

    # Test API Key
    try:
        headers = {'X-API-Key': 'my-api-key-123'}
        response = requests.get(
            'https://httpbin.org/headers',
            headers=headers
        )
        print("API Key Test:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"API Key Error: {e}\n")

if __name__ == "__main__":
    test_auth_methods()
```

**Note:** In Postman, you can click the "Code" button (</>) to see the Python code for any request you've configured.

### Step 11: Asynchronous Programming with asyncio
Learn how to make concurrent API requests using Python's asyncio and aiohttp.

Here's how to make asynchronous API requests:

```python
import asyncio
import aiohttp
import requests
import time

async def fetch_post(session, post_id):
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    async with session.get(url) as response:
        return await response.json()

async def fetch_user(session, user_id):
    url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    async with session.get(url) as response:
        return await response.json()

async def main():
    # Start timing
    start_time = time.time()
    
    # Create a session
    async with aiohttp.ClientSession() as session:
        # Create tasks for multiple API calls
        post_tasks = [fetch_post(session, i) for i in range(1, 6)]
        user_tasks = [fetch_user(session, i) for i in range(1, 4)]
        
        # Execute all tasks concurrently
        posts, users = await asyncio.gather(
            asyncio.gather(*post_tasks),
            asyncio.gather(*user_tasks)
        )
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Print results
        print(f"\nFetched {len(posts)} posts and {len(users)} users in {execution_time:.2f} seconds")
        
        print("\nPosts:")
        for post in posts:
            print(f"- Post {post['id']}: {post['title'][:30]}...")
        
        print("\nUsers:")
        for user in users:
            print(f"- User {user['id']}: {user['name']}")

# Compare with synchronous version
def sync_version():
    start_time = time.time()
    
    # Make the same requests synchronously
    posts = []
    users = []
    
    for i in range(1, 6):
        response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{i}')
        posts.append(response.json())
    
    for i in range(1, 4):
        response = requests.get(f'https://jsonplaceholder.typicode.com/users/{i}')
        users.append(response.json())
    
    execution_time = time.time() - start_time
    print(f"\nSynchronous version took {execution_time:.2f} seconds")

if __name__ == "__main__":
    print("Running async version...")
    asyncio.run(main())
    
    print("\nRunning sync version...")
    sync_version()
```

This example demonstrates:
1. Creating concurrent requests using `asyncio` and `aiohttp`
2. Fetching multiple posts and users simultaneously
3. Comparing async vs sync performance
4. Proper session management and error handling

Expected output will look something like:
```
Running async version...
Fetched 5 posts and 3 users in 0.34 seconds

Posts:
- Post 1: sunt aut facere repellat pr...
- Post 2: qui est esse...
- Post 3: ea molestias quasi exercita...
- Post 4: eum et est occaecati...
- Post 5: nesciunt quas odio...

Users:
- User 1: Leanne Graham
- User 2: Ervin Howell
- User 3: Clementine Bauch

Running sync version...
Synchronous version took 1.52 seconds
```

The async version is typically 3-4 times faster because it makes all requests concurrently instead of sequentially.

### Additional Resources:
- [Requests Library Documentation](https://docs.python-requests.org/)
- [JSONPlaceholder API Documentation](https://jsonplaceholder.typicode.com/)
- [HTTP Status Codes Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
