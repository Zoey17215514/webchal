from flask import Flask, request, render_template_string, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "not_secret"

# Simple index
@app.route('/')
def index():
    return """
    <h1>Welcome to Template Trouble</h1>
    <p>Try the <a href="/search">search</a>.</p>
    """

# Vulnerable search (SSTI)
@app.route('/search')
def search():
    q = request.args.get('q', '')
    # WARNING: intentionally vulnerable to SSTI for the challenge
    template = """
    <h2>Search results for: {{q}}</h2>
    <p>We did a deep search... (not really)</p>
    <form action="/search" method="get">
      <input name="q" placeholder="search..." value="{{q}}">
      <button type="submit">Search</button>
    </form>
    """
    # render_template_string uses Jinja2; passing `q` but also allowing template injection
    # By putting user input into the template context, the app is vulnerable.
    return render_template_string(template.replace("{{q}}", q), q=q)

# small admin page to make things look real (not linked)
@app.route('/admin')
def admin():
    return "<h1>Admin panel</h1><p>Only admins can see flags. (Not for players)</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
