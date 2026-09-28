# Deployment Guide
## CampusEnroll – Student Course Registration System

This guide provides step-by-step instructions to deploy CampusEnroll to production cloud hosting platforms (Render, Railway, PythonAnywhere, or Docker).

---

### Option 1: Free Cloud Deployment on Render.com (Recommended)

[Render](https://render.com) offers free web service hosting for Python web apps.

1. **Push your project to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of CampusEnroll"
   git remote add origin https://github.com/<your-username>/campus-enroll.git
   git branch -M main
   git push -u origin main
   ```

2. **Create a new Web Service on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) and log in with your GitHub account.
   - Click **"New +"** and choose **"Web Service"**.
   - Select your `campus-enroll` repository.

3. **Configure the Web Service**:
   - **Name**: `campus-enroll`
   - **Region**: Choose the closest region (e.g., Singapore, Frankfurt, or Oregon).
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python database/init_db.py
     ```
   - **Start Command**:
     ```bash
     gunicorn wsgi:app
     ```
   - **Plan**: `Free`

4. **Environment Variables**:
   Under the **Environment Variables** tab, add:
   - `SECRET_KEY`: `your_random_production_secret_key_here`
   - `FLASK_DEBUG`: `False`

5. **Deploy**:
   - Click **"Create Web Service"**.
   - Render will build the environment, initialize the SQLite database, and launch Gunicorn.
   - Your live URL will be ready at: `https://campus-enroll.onrender.com`.

---

### Option 2: Deployment with Docker (Any VPS / Local Server)

You can run CampusEnroll in an isolated Docker container anywhere:

1. **Build the Docker Image**:
   ```bash
   docker build -t campusenroll .
   ```

2. **Run the Container**:
   ```bash
   docker run -d -p 5000:5000 --name campusenroll_app campusenroll
   ```

3. **Access the Application**:
   Navigate to `http://localhost:5000` (or `http://<server-ip>:5000`).

---

### Option 3: Production Deployment on Windows Server (Waitress)

On Windows servers where Gunicorn is not natively supported, run with `Waitress`:

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Initialize database:
   ```powershell
   python database/init_db.py
   ```
3. Run with Waitress WSGI:
   ```powershell
   python -c "from waitress import serve; from app import app; serve(app, host='0.0.0.0', port=5000)"
   ```

---

### Option 4: Deploying on PythonAnywhere

1. Sign up for a free account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Open a Bash console and upload your files (or git clone).
3. Set up a virtual environment and install `requirements.txt`.
4. Run `python database/init_db.py`.
5. In the **Web** tab, configure:
   - Source code directory: `/home/<username>/campus-enroll`
   - WSGI configuration file: point to `from app import app as application`
6. Click **Reload** to make your site live at `<username>.pythonanywhere.com`.
