from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuario"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validaciones
        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/register.html')
        
        # Crear usuario
        user, error = User.create(nombre, email, password)
        
        if error:
            flash(error, 'danger')
            return render_template('auth/register.html')
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Por favor ingresa email y contraseña', 'danger')
            return render_template('auth/login.html')
        
        user = User.get_by_email(email)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.nombre
            flash(f'Bienvenido, {user.nombre}!', 'success')
            return redirect(url_for('contact.list'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/profile')
def profile():
    """Perfil del usuario"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.get_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return render_template('auth/profile.html', user=user)

@bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))