# StackBlog: StackOverflow Blog Generator

This project is an automated solution for generating detailed and informative blog posts based on Stack Overflow discussions. Using CrewAI and multiple AI agents, it extracts relevant information from Stack Overflow, compiles it into comprehensive reports, and formats it into engaging blog posts.

Can be deployed on Heroku in a few steps 🚀

# Setup

### Prerequisites

```sh
# Clone the repository
git clone https://github.com/SuperMuel/blog_generator_from_stackoverflow.git

cd blog_generator_from_stackoverflow

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### API Keys

You need an Anthropic API key to generate blog posts. You can get one by signing up at [Anthropic](https://www.anthropic.com/api).

To search for StackOverflow posts, you need a Serper.dev API key. You can get one by signing up at [Serper.dev](https://serper.dev/).

Once you have the API keys, copy the `.env.example` file to `.env` and add your API keys:

```env
ANTHROPIC_API_KEY="Your Anthropic API"
SERPER_API_KEY="Your Serper api"
```

# Run the application

## Locally

1. **Start the Flask application**:

   ```sh
   python api.py
   ```

2. **Test the API**:

   You can test the endpoint using `curl` or Postman:

```sh
curl -X POST http://127.0.0.1:5000/generate-article \
    -H "Content-Type: application/json" \
    -d '{"topic": "La programmation asynchrone en Python", "language": "French"}'
```

## On Heroku

### Setup Heroku

If you haven't already, install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli).

1. **Login to Heroku**:

```sh
heroku login
```

2. **Create a new Heroku app**:

Inside the project directory, run:

```sh
heroku create your-app-name
```

3. Set the environment variables on Heroku:

```sh
python setup_heroku.py
```

4. **Deploy the application**:

```sh
git push heroku main
```

5. **Scale the application**:

This will start a web dyno to serve the application.

```sh
heroku ps:scale web=1
```

6. **Open the application**:

```sh
heroku open
```

# API Endpoints

## Generate Article

- **Endpoint**: `/generate-article`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "topic": "Your topic here",
    "language": "Language code here (e.g., 'EN', 'FR')"
  }
  ```
- **Response**:
  ```json
  {
    "article": "Generated article content here"
  }
  ```
