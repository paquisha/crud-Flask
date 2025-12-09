from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.contact import Contact

bp = Blueprint('contact', __name__, url_prefix='/contactos')

def login_required(f):
    """Decorador para requerir autenticación"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    
    return decorated_function

@bp.route('/')
@login_required
def list():
    """Listar contactos del usuario"""
    user_id = session['user_id']
    contacts = Contact.get_all_by_user(user_id)
    return render_template('contacts/list.html', contacts=contacts)

@bp.route('/agregar', methods=['GET', 'POST'])
@login_required
def add():
    """Agregar nuevo contacto"""
    if request.method == 'POST':
        user_id = session['user_id']
        contact = Contact(
            user_id=user_id,
            nombre=request.form.get('nombre', '').strip(),
            correo=request.form.get('correo', '').strip(),
            telefono=request.form.get('telefono', '').strip(),
            detalle=request.form.get('detalle', '').strip()
        )
        
        success, errors = contact.save()
        
        if success:
            flash('Contacto agregado exitosamente', 'success')
            return redirect(url_for('contact.list'))
        else:
            for error in errors:
                flash(error, 'danger')
    
    return render_template('contacts/add.html')

@bp.route('/editar/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def edit(contact_id):
    """Editar contacto existente"""
    user_id = session['user_id']
    contact = Contact.get_by_id(contact_id, user_id)
    
    if not contact:
        flash('Contacto no encontrado', 'danger')
        return redirect(url_for('contact.list'))
    
    if request.method == 'POST':
        contact.nombre = request.form.get('nombre', '').strip()
        contact.correo = request.form.get('correo', '').strip()
        contact.telefono = request.form.get('telefono', '').strip()
        contact.detalle = request.form.get('detalle', '').strip()
        
        success, errors = contact.save()
        
        if success:
            flash('Contacto actualizado exitosamente', 'success')
            return redirect(url_for('contact.list'))
        else:
            for error in errors:
                flash(error, 'danger')
    
    return render_template('contacts/edit.html', contact=contact)

@bp.route('/eliminar/<int:contact_id>')
@login_required
def delete(contact_id):
    """Eliminar contacto"""
    user_id = session['user_id']
    contact = Contact.get_by_id(contact_id, user_id)
    
    if contact and contact.delete():
        flash('Contacto eliminado exitosamente', 'success')
    else:
        flash('No se pudo eliminar el contacto', 'danger')
    
    return redirect(url_for('contact.list'))