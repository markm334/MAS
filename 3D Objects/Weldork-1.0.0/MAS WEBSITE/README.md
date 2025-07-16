# MAS WEBSITE

This is a Django project named `maswebsite` with a main app called `mainapp`.

## Getting Started

1. **Install dependencies:**
   - Django is already installed in your environment.
2. **Run migrations:**
   ```powershell
   C:/Users/TALON/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py migrate
   ```
3. **Run the development server:**
   ```powershell
   C:/Users/TALON/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py runserver
   ```
4. **Create a superuser (optional):**
   ```powershell
   C:/Users/TALON/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py createsuperuser
   ```

## Project Structure
- `maswebsite/` - Django project settings and configuration
- `mainapp/` - Main Django app for your project

## Customization
- Add your models, views, and templates in `mainapp`.
- Update `maswebsite/settings.py` to register new apps or middleware as needed.

---

For more information, see the [Django documentation](https://docs.djangoproject.com/en/stable/).
