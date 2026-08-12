from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import json
from datetime import datetime, timedelta, time
from .models import Medico, Paciente, Personal, SignoVital, Consulta, TicketSoporte, Cita


# --- HERRAMIENTA GLOBAL PARA VALIDAR TURNOS ---
def verificar_horario(horario_str):
    if not horario_str or '-' not in horario_str:
        return True 
        
    try:
        inicio_str, fin_str = horario_str.split('-')
        hora_inicio = datetime.strptime(inicio_str.strip(), "%H:%M").time()
        hora_fin = datetime.strptime(fin_str.strip(), "%H:%M").time()
        hora_actual = datetime.now().time()
        
        if hora_inicio <= hora_fin:
            return hora_inicio <= hora_actual <= hora_fin
        else: 
            return hora_actual >= hora_inicio or hora_actual <= hora_fin
    except ValueError:
        return True 
# ----------------------------------------------


def generar_horarios_medico(medico, fecha_consulta):
    horario_str = getattr(medico, 'horario', '08:00 - 16:00')
    if not horario_str:
        horario_str = '08:00 - 16:00'
        
    try:
        partes = horario_str.split('-')
        h_ini = int(partes[0].strip().split(':')[0])
        m_ini = int(partes[0].strip().split(':')[1])
        h_fin = int(partes[1].strip().split(':')[0])
        m_fin = int(partes[1].strip().split(':')[1])
    except Exception:
        h_ini, m_ini = 8, 0
        h_fin, m_fin = 16, 0

    if h_ini >= 24: h_ini = 0
    if h_fin >= 24: h_fin = 23

    curr = datetime.combine(fecha_consulta, time(h_ini, m_ini))
    end = datetime.combine(fecha_consulta, time(h_fin, m_fin))

    if end <= curr:
        end += timedelta(days=1)

    citas_ocupadas = Cita.objects.filter(medico=medico, fecha=fecha_consulta).values_list('hora', flat=True)
    ocupadas_set = {c.strftime("%H:%M") for c in citas_ocupadas if c}

    emergencias_hoy = Cita.objects.filter(medico=medico, fecha=fecha_consulta, motivo__icontains='EMERGENCIA')
    doctor_bloqueado = False
    
    for em in emergencias_hoy:
        atendido = Consulta.objects.filter(paciente=em.paciente).exists()
        if not atendido:
            doctor_bloqueado = True
            break

    ahora = datetime.now()
    slots = []
    
    while curr < end:
        slot_str = curr.strftime("%H:%M")
        es_ocupado = (slot_str in ocupadas_set) or doctor_bloqueado or (curr < ahora)
        
        slots.append({
            'hora': slot_str,
            'hora_12': curr.strftime("%I:%M %p"), 
            'ocupado': es_ocupado
        })
        curr += timedelta(minutes=30)

    return slots


def obtener_horarios_ajax(request):
    medico_id = request.GET.get('medico_id')
    fecha_str = request.GET.get('fecha')
    
    if not medico_id or not fecha_str:
        return JsonResponse({'slots': []})
        
    try:
        fecha_cita = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        medico = Medico.objects.get(id=medico_id)
        slots = generar_horarios_medico(medico, fecha_cita)
        return JsonResponse({'slots': slots})
    except Exception as e:
        return JsonResponse({'slots': []})


# Módulo 1: Login
def login_vista(request):
    if request.method == 'POST':
        rol = request.POST.get('rol')
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        if rol == 'administrador' and usuario == 'admin' and password == 'admin123':
            return redirect('administrador')
        
        elif rol == 'medico':
            medico_obj = Medico.objects.filter(usuario=usuario, password=password).first()
            if medico_obj:
                request.session['medico_id'] = medico_obj.id 
                return redirect('medico')
                
        else:
            personal_obj = Personal.objects.filter(rol=rol, usuario=usuario, password=password).first()
            if personal_obj:
                request.session[f'{rol}_id'] = personal_obj.id
                return redirect(rol)

        return render(request, 'login.html', {'error': 'Usuario o contraseña no encontrados en la base de datos.'})
    
    return render(request, 'login.html')


# Módulo 2: Panel Recepción 
def recepcion_vista(request):
    recepcion_id = request.session.get('recepcion_id')
    if not recepcion_id:
        return redirect('login')
        
    recepcionista_actual = Personal.objects.get(id=recepcion_id)
    
    # CALCULAMOS SI ESTÁ EN TURNO
    en_turno = verificar_horario(recepcionista_actual.horario)
    
    fecha_hoy = datetime.today().date()
    medicos_list = Medico.objects.all()
    
    if request.method == 'POST':
        if not en_turno:
            return redirect('recepcion')

        accion = request.POST.get('accion')

        if accion == 'registrar_paciente' or accion == 'nuevo_paciente':
            curp = request.POST.get('curp', '').upper()
            telefono = request.POST.get('telefono', '').strip()
        
            if len(curp) != 18:
                messages.error(request, 'El CURP debe tener exactamente 18 caracteres.')
            elif Paciente.objects.filter(curp=curp).exists():
                messages.error(request, f'Ya existe un paciente registrado con la CURP: {curp}')
            elif Paciente.objects.filter(telefono=telefono).exists():
                # 🔍 NUEVA VALIDACIÓN: Evita números de teléfono duplicados
                messages.error(request, f'Ya existe un paciente registrado con el teléfono: {telefono}')
            else:
                edad_input = request.POST.get('edad')
                edad_val = int(edad_input) if edad_input and edad_input.isdigit() else None
                genero_val = request.POST.get('genero')

                Paciente.objects.create(
                nombre=request.POST.get('nombre'),
                apellido_paterno=request.POST.get('apellido_paterno'),
                apellido_materno=request.POST.get('apellido_materno', ''),
                edad=edad_val,
                genero=genero_val,
                curp=curp,
                telefono=telefono,
                tipo_sangre=request.POST.get('tipo_sangre')
                )
                messages.success(request, 'Paciente registrado con éxito.')

        elif accion == 'agendar_cita':
            paciente_id = request.POST.get('paciente_id')
            medico_id = request.POST.get('medico_id')
            hora_solicitada = request.POST.get('hora')
            motivo = request.POST.get('motivo')
            fecha_solicitada_str = request.POST.get('fecha_cita')

            if not hora_solicitada or not fecha_solicitada_str:
                messages.error(request, 'Por favor seleccione una fecha y un bloque de horario disponible.')
            else:
                fecha_solicitada = datetime.strptime(fecha_solicitada_str, '%Y-%m-%d').date()
                
                try:
                    hora_obj = datetime.strptime(hora_solicitada, '%H:%M').time()
                    dt_solicitada = datetime.combine(fecha_solicitada, hora_obj)
                    if dt_solicitada < datetime.now():
                        messages.error(request, '⚠️ Error: No puedes agendar una cita en un horario o fecha que ya pasó.')
                        return redirect('recepcion')
                except Exception:
                    if fecha_solicitada < fecha_hoy:
                        messages.error(request, '⚠️ Error: No puedes agendar citas en fechas pasadas.')
                        return redirect('recepcion')

                medico = Medico.objects.get(id=medico_id)
                paciente = Paciente.objects.get(id=paciente_id)
                
                if Cita.objects.filter(paciente=paciente, fecha=fecha_solicitada).exists():
                    messages.error(request, f'⚠️ Error: El paciente ya tiene una cita agendada para ese día.')
                elif Cita.objects.filter(medico=medico, hora=hora_solicitada, fecha=fecha_solicitada).exists():
                    messages.error(request, f'El bloque de las {hora_solicitada} ya fue reservado.')
                else:
                    Cita.objects.create(
                        paciente=paciente, medico=medico, hora=hora_solicitada, motivo=motivo, fecha=fecha_solicitada
                    )
                    messages.success(request, f'Cita agendada exitosamente a las {hora_solicitada} el {fecha_solicitada}.')

        elif accion == 'ingreso_emergencia' or accion == 'emergencia':
            ahora = datetime.now()
            hora_asignada = ahora.strftime("%H:%M")
            
            mejor_medico = None
            medicos_disponibles = []
            
            for doc in medicos_list:
                # 🔍 USAMOS LA FUNCIÓN GLOBAL QUE YA TIENES ARRIBA:
                if verificar_horario(doc.horario):
                    emergencias_activas = Cita.objects.filter(medico=doc, fecha=fecha_hoy, motivo__icontains='EMERGENCIA')
                    doctor_bloqueado = False
                    for em in emergencias_activas:
                        if not Consulta.objects.filter(paciente=em.paciente).exists():
                            doctor_bloqueado = True
                            break
                    if not doctor_bloqueado:
                        medicos_disponibles.append(doc)
            
            if medicos_disponibles:
                mejor_medico = min(medicos_disponibles, key=lambda m: Cita.objects.filter(medico=m, fecha=fecha_hoy, estado='En Espera').count())
                
                citas_afectadas = Cita.objects.filter(medico=mejor_medico, fecha=fecha_hoy, estado='En Espera')
                for cita in citas_afectadas:
                    cita.estado = 'Espera Extra (Emergencia)'
                    cita.save()

                curp_emergencia = f"EMER{ahora.strftime('%Y%m%d%H%M%S')}" 
                total_desconocidos = Paciente.objects.filter(curp__startswith='EMER').count() + 1
                nombre_generado = f"Desconocido {total_desconocidos}"
                
                paciente_desconocido = Paciente.objects.create(
                    nombre=nombre_generado, apellido_paterno="Paciente", apellido_materno="Emergencia",
                    curp=curp_emergencia, telefono="0000000000", tipo_sangre="N/A"
                )
                
                Cita.objects.create(
                    paciente=paciente_desconocido, medico=mejor_medico, hora=hora_asignada,
                    motivo="🚨 EMERGENCIA MÉDICA (Sin Identificar)", fecha=fecha_hoy
                )
                messages.success(request, f'🚨 PROTOCOLO ACTIVADO: {nombre_generado} ingresado con el Dr(a). {mejor_medico.nombre}.')
            else:
                messages.error(request, '⚠️ CÓDIGO NEGRO: No hay médicos en turno en este horario o están en código rojo.')

        elif accion == 'cancelar_cita':
            cita_id = request.POST.get('cita_id')
            try:
                cita = Cita.objects.get(id=cita_id)
                if 'EMERGENCIA' in cita.motivo:
                    messages.error(request, '⚠️ Acción denegada: No puedes cancelar una emergencia en curso.')
                else:
                    nombre_paciente = cita.paciente.nombre
                    cita.delete()
                    messages.success(request, f'✅ La cita de {nombre_paciente} ha sido cancelada correctamente.')
            except Cita.DoesNotExist:
                messages.error(request, '⚠️ Error: La cita ya no existe.')

        elif accion == 'nuevo_ticket':
            TicketSoporte.objects.create(
                empleado=request.POST.get('empleado'),
                area=request.POST.get('area', 'Recepción'),
                falla=request.POST.get('falla')
            )
            messages.success(request, '🎫 Tu reporte ha sido enviado a Sistemas exitosamente.')

        return redirect('recepcion')

    contexto = {
        'recepcionista': recepcionista_actual,
        'pacientes': Paciente.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre'),
        'pacientes_agendar': Paciente.objects.exclude(curp__startswith='EMER').order_by('apellido_paterno', 'apellido_materno', 'nombre'),
        'pacientes_directorio': Paciente.objects.all().order_by('apellido_paterno', 'apellido_materno', 'nombre'),
        'medicos': medicos_list,
        'citas_hoy': Cita.objects.filter(fecha=fecha_hoy).order_by('hora'),
        'en_turno': en_turno 
    }
    return render(request, 'recepcion.html', contexto)


# Módulo 4: Panel Médico
def medico_vista(request):
    medico_id = request.session.get('medico_id')
    
    if not medico_id:
        return redirect('login')
        
    medico_actual = Medico.objects.get(id=medico_id)
    fecha_hoy = datetime.today().date()
    
    # CALCULAMOS SI ESTÁ EN TURNO
    en_turno = verificar_horario(medico_actual.horario)

    if request.method == 'POST':
        if not en_turno:
            return redirect('medico')

        accion = request.POST.get('accion')

        if accion == 'nuevo_ticket':
            TicketSoporte.objects.create(
                empleado=request.POST.get('empleado'),
                area=request.POST.get('area', 'Consultorio Médico'),
                falla=request.POST.get('falla')
            )
            messages.success(request, '🎫 Tu reporte ha sido enviado a Sistemas exitosamente.')
        else: 
            paciente_id = request.POST.get('paciente_id')
            if paciente_id:
                paciente_obj = Paciente.objects.get(id=paciente_id)
                
                Consulta.objects.create(
                    paciente=paciente_obj,
                    medico_nombre=f"Dr(a). {medico_actual.nombre}",
                    diagnostico=request.POST.get('diagnostico'),
                    receta=request.POST.get('receta')
                )
                
                Cita.objects.filter(paciente=paciente_obj, medico=medico_actual, fecha=fecha_hoy).delete()
                
                messages.success(request, f'✅ Consulta guardada y receta emitida para {paciente_obj.nombre}.')

        return redirect('medico')

    citas_asignadas = Cita.objects.filter(medico=medico_actual, fecha=fecha_hoy).order_by('hora')
    hay_emergencia = citas_asignadas.filter(motivo__icontains='EMERGENCIA').exists()

    # ⏰ VALIDAR SI AÚN NO ES LA HORA DE LA CITA
    hora_actual = datetime.now().time()
    for cita in citas_asignadas:
        if 'EMERGENCIA' in cita.motivo:
            cita.fuera_de_hora = False
        else:
            try:
                if isinstance(cita.hora, str):
                    hora_clean = cita.hora.lower().replace('p.m.', '').replace('a.m.', '').strip()
                    hora_cita = datetime.strptime(hora_clean, "%H:%M").time()
                else:
                    hora_cita = cita.hora
                cita.fuera_de_hora = hora_cita > hora_actual
            except:
                cita.fuera_de_hora = False

    pacientes_en_cola = [cita.paciente for cita in citas_asignadas]
    signos_asignados = SignoVital.objects.filter(paciente__in=pacientes_en_cola).order_by('-fecha')
    consultas_doctor = Consulta.objects.filter(medico_nombre=f"Dr(a). {medico_actual.nombre}").order_by('-fecha')

    contexto = {
        'medico': medico_actual,
        'citas_asignadas': citas_asignadas,
        'signos': signos_asignados,
        'consultas': consultas_doctor,
        'en_turno': en_turno,
        'hay_emergencia': hay_emergencia  
    }
    return render(request, 'medico.html', contexto)


# Módulo 5: Panel Enfermería
def enfermeria_vista(request):
    enfermeria_id = request.session.get('enfermeria_id')
    if not enfermeria_id:
        return redirect('login')

    enfermero_actual = Personal.objects.get(id=enfermeria_id)
    
    # CALCULAMOS SI ESTÁ EN TURNO
    en_turno = verificar_horario(enfermero_actual.horario)

    if request.method == 'POST':
        if not en_turno:
            return redirect('enfermeria')

        accion = request.POST.get('accion')

        if accion == 'guardar_signos':
            paciente_id = request.POST.get('paciente_id')
            presion = request.POST.get('presion')
            
            try:
                temperatura = float(request.POST.get('temperatura'))
                peso = float(request.POST.get('peso'))
                estatura = float(request.POST.get('estatura'))
                oxigenacion = int(request.POST.get('oxigenacion'))
            except ValueError:
                messages.error(request, '⚠️ Error: Todos los campos numéricos deben contener valores válidos.')
                return redirect('enfermeria')

            errores_biologicos = []
            
            try:
                sistolica, diastolica = map(int, presion.split('/'))
                if not (50 <= sistolica <= 250) or not (30 <= diastolica <= 150):
                    errores_biologicos.append("Presión arterial fuera de rangos humanos posibles (Sis: 50-250, Dia: 30-150).")
            except:
                errores_biologicos.append("Formato de presión inválido. Use exactamente el formato XXX/XX (Ej: 120/80).")

            if not (30.0 <= temperatura <= 45.0):
                errores_biologicos.append("Temperatura incompatible con la vida (Mín: 30°C, Máx: 45°C).")
            if not (2.0 <= peso <= 350.0):
                errores_biologicos.append("Peso registrado irreal (Mín: 2kg, Máx: 350kg).")
            if not (0.40 <= estatura <= 2.50):
                errores_biologicos.append("Estatura registrada irreal (Mín: 0.40m, Máx: 2.50m).")
            if not (30 <= oxigenacion <= 100):
                errores_biologicos.append("Nivel de oxigenación fuera de rango (Mín: 30%, Máx: 100%).")

            if errores_biologicos:
                for err in errores_biologicos:
                    messages.error(request, f'⛔ {err}')
                return redirect('enfermeria')

            if paciente_id:
                paciente_obj = Paciente.objects.get(id=paciente_id)
                registro_existente = SignoVital.objects.filter(paciente=paciente_obj).first()
                
                if registro_existente:
                    registro_existente.presion = presion
                    registro_existente.temperatura = temperatura
                    registro_existente.peso = peso
                    registro_existente.estatura = estatura
                    registro_existente.oxigenacion = oxigenacion
                    registro_existente.fecha = datetime.now() 
                    registro_existente.save()
                    messages.success(request, f'🔄 El expediente de signos vitales de {paciente_obj.nombre} ha sido ACTUALIZADO con éxito.')
                else:
                    SignoVital.objects.create(
                        paciente=paciente_obj, presion=presion, temperatura=temperatura,
                        peso=peso, estatura=estatura, oxigenacion=oxigenacion
                    )
                    messages.success(request, f'✅ Expediente de signos vitales creado para {paciente_obj.nombre}.')

        elif accion == 'actualizar_paciente':
            paciente_id = request.POST.get('paciente_id')
            curp_nueva = request.POST.get('curp', '').upper()
            telefono_nuevo = request.POST.get('telefono', '').strip()
            
            if paciente_id:
                paciente_obj = Paciente.objects.get(id=paciente_id)

                # 1. Validar longitud de CURP
                if len(curp_nueva) != 18:
                    messages.error(request, '⚠️ Error: El CURP debe tener exactamente 18 caracteres.')
                    return redirect('enfermeria')

                # 2. Validar formato de Teléfono (10 dígitos)
                if len(telefono_nuevo) != 10 or not telefono_nuevo.isdigit():
                    messages.error(request, '⚠️ Error: El teléfono debe contener exactamente 10 dígitos numéricos.')
                    return redirect('enfermeria')

                # 3. Validar CURP duplicada en otro paciente
                if Paciente.objects.filter(curp=curp_nueva).exclude(id=paciente_obj.id).exists():
                    messages.error(request, f'⚠️ Error: La CURP "{curp_nueva}" ya pertenece a otro paciente registrado.')
                    return redirect('enfermeria')

                # 4. Validar Teléfono duplicado en otro paciente
                if Paciente.objects.filter(telefono=telefono_nuevo).exclude(id=paciente_obj.id).exists():
                    messages.error(request, f'⚠️ Error: El teléfono "{telefono_nuevo}" ya está registrado con otro paciente.')
                    return redirect('enfermeria')

                # Si pasa las validaciones, actualiza los datos:
                edad_input = request.POST.get('edad')
                genero_input = request.POST.get('genero')
                
                paciente_obj.nombre = request.POST.get('nombre')
                paciente_obj.apellido_paterno = request.POST.get('apellido_paterno')
                paciente_obj.apellido_materno = request.POST.get('apellido_materno', '')
                
                if edad_input and edad_input.isdigit():
                    paciente_obj.edad = int(edad_input)
                if genero_input:
                    if genero_input == 'M': paciente_obj.genero = 'Masculino'
                    elif genero_input == 'F': paciente_obj.genero = 'Femenino'
                    else: paciente_obj.genero = genero_input
                    
                paciente_obj.curp = curp_nueva
                paciente_obj.telefono = telefono_nuevo
                paciente_obj.tipo_sangre = request.POST.get('tipo_sangre')
                paciente_obj.save()

                # Actualizar motivo de la cita para quitar la leyenda de no identificado
                citas_activas = Cita.objects.filter(paciente=paciente_obj)
                for cita in citas_activas:
                    if "(Sin Identificar)" in cita.motivo:
                        cita.motivo = cita.motivo.replace(" (Sin Identificar)", "")
                        cita.save()

                messages.success(request, '🏥 ¡Identidad confirmada! Expediente y monitor de citas actualizados.')

        elif accion == 'nuevo_ticket':
            TicketSoporte.objects.create(
                empleado=request.POST.get('empleado'),
                area=request.POST.get('area', 'Enfermería'),
                falla=request.POST.get('falla')
            )
            messages.success(request, '🎫 Tu reporte ha sido enviado a Sistemas exitosamente.')

        return redirect('enfermeria')

    contexto = {
        'enfermero': enfermero_actual,
        'pacientes': Paciente.objects.all(),
        'pacientes_desconocidos': Paciente.objects.filter(curp__startswith='EMER'),
        'signos': SignoVital.objects.all().order_by('-fecha'),
        'en_turno': en_turno 
    }
    return render(request, 'enfermeria.html', contexto)


# Módulo 6: Administrador
def administrador_vista(request):
    def usuario_existe(usr, exclude_medico_id=None, exclude_personal_id=None):
        m_query = Medico.objects.filter(usuario=usr)
        if exclude_medico_id: m_query = m_query.exclude(id=exclude_medico_id)
        p_query = Personal.objects.filter(usuario=usr)
        if exclude_personal_id: p_query = p_query.exclude(id=exclude_personal_id)
        return m_query.exists() or p_query.exists()

    def password_existe(pwd, exclude_medico_id=None, exclude_personal_id=None):
        m_query = Medico.objects.filter(password=pwd)
        if exclude_medico_id: m_query = m_query.exclude(id=exclude_medico_id)
        p_query = Personal.objects.filter(password=pwd)
        if exclude_personal_id: p_query = p_query.exclude(id=exclude_personal_id)
        return m_query.exists() or p_query.exists()

    def telefono_existe(tel, exclude_medico_id=None, exclude_personal_id=None):
        if not tel:
            return False
        m_query = Medico.objects.filter(telefono=tel)
        if exclude_medico_id: m_query = m_query.exclude(id=exclude_medico_id)
        p_query = Personal.objects.filter(telefono=tel)
        if exclude_personal_id: p_query = p_query.exclude(id=exclude_personal_id)
        return m_query.exists() or p_query.exists()

    def cedula_existe(ced, exclude_medico_id=None):
        if not ced:
            return False
        m_query = Medico.objects.filter(cedula=ced)
        if exclude_medico_id:
            m_query = m_query.exclude(id=exclude_medico_id)
        return m_query.exists()

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'nuevo_ticket':
            TicketSoporte.objects.create(
                empleado=request.POST.get('empleado', 'Super Administrador'),
                area=request.POST.get('area', 'Administración'),
                falla=request.POST.get('falla')
            )
            messages.success(request, '🎫 Reporte de falla enviado exitosamente a Soporte Técnico.')
            return redirect('administrador')

        if accion in ['crear_empleado', 'editar_medico', 'editar_personal']:
            h_inicio_str = request.POST.get('hora_inicio')
            h_fin_str = request.POST.get('hora_fin')
            
            h_in = int(h_inicio_str.split(':')[0])
            h_out = int(h_fin_str.split(':')[0])
            
            if h_out >= h_in: 
                horas_trabajadas = h_out - h_in
            else: 
                horas_trabajadas = (24 - h_in) + h_out

            if horas_trabajadas < 4:
                messages.error(request, f"⚠️ Error: La jornada laboral es muy corta ({horas_trabajadas} hrs). El mínimo permitido es de 4 horas.")
                return redirect('administrador')
                
            if horas_trabajadas > 8:
                messages.error(request, f"⚠️ Error: La jornada laboral excede el límite ({horas_trabajadas} hrs). El máximo permitido es de 8 horas.")
                return redirect('administrador')

        if accion == 'crear_empleado':
            usuario = request.POST.get('usuario')
            password = request.POST.get('password')
            telefono = request.POST.get('telefono')
            rol = request.POST.get('rol')
            cedula_val = request.POST.get('cedula', '00000')
            
            if usuario_existe(usuario):
                messages.error(request, f"⚠️ Error: El usuario '{usuario}' ya está en uso.")
                return redirect('administrador')
            if password_existe(password):
                messages.error(request, "⚠️ Error: Esa contraseña ya está en uso.")
                return redirect('administrador')
            if telefono_existe(telefono):
                messages.error(request, f"⚠️ Error: El teléfono '{telefono}' ya pertenece a otro registro.")
                return redirect('administrador')
            if rol == 'medico' and cedula_existe(cedula_val):
                messages.error(request, f"⚠️ Error: La cédula profesional '{cedula_val}' ya pertenece a otro médico.")
                return redirect('administrador')

            horario_completo = f"{request.POST.get('hora_inicio')} - {request.POST.get('hora_fin')}"
            
            if rol == 'medico':
                Medico.objects.create(
                    nombre=request.POST.get('nombre'), especialidad=request.POST.get('especialidad', 'General'),
                    cedula=cedula_val, telefono=telefono,
                    horario=horario_completo, usuario=usuario, password=password
                )
            else:
                Personal.objects.create(
                    nombre=request.POST.get('nombre'), rol=rol, telefono=telefono,
                    horario=horario_completo, usuario=usuario, password=password
                )
            messages.success(request, "✅ Empleado registrado exitosamente.")

        elif accion == 'editar_medico':
            m_id = request.POST.get('id')
            m = Medico.objects.get(id=m_id)
            
            nuevo_usr = request.POST.get('usuario')
            nueva_pwd = request.POST.get('password')
            nuevo_tel = request.POST.get('telefono')
            nueva_ced = request.POST.get('cedula', getattr(m, 'cedula', '00000'))

            if usuario_existe(nuevo_usr, exclude_medico_id=m.id):
                messages.error(request, f"⚠️ Error: El usuario '{nuevo_usr}' ya pertenece a otro registro.")
                return redirect('administrador')
            if password_existe(nueva_pwd, exclude_medico_id=m.id):
                messages.error(request, "⚠️ Error: Esa contraseña ya pertenece a otro registro.")
                return redirect('administrador')
            if telefono_existe(nuevo_tel, exclude_medico_id=m.id):
                messages.error(request, f"⚠️ Error: El teléfono '{nuevo_tel}' ya pertenece a otro registro.")
                return redirect('administrador')
            if cedula_existe(nueva_ced, exclude_medico_id=m.id):
                messages.error(request, f"⚠️ Error: La cédula profesional '{nueva_ced}' ya pertenece a otro médico.")
                return redirect('administrador')

            m.nombre = request.POST.get('nombre')
            m.especialidad = request.POST.get('especialidad', m.especialidad)
            m.cedula = nueva_ced
            m.telefono = nuevo_tel
            m.horario = f"{request.POST.get('hora_inicio')} - {request.POST.get('hora_fin')}"
            m.usuario = nuevo_usr
            m.password = nueva_pwd
            m.save()
            messages.success(request, "✅ Médico actualizado correctamente.")

        elif accion == 'editar_personal':
            p_id = request.POST.get('id')
            p = Personal.objects.get(id=p_id)

            nuevo_usr = request.POST.get('usuario')
            nueva_pwd = request.POST.get('password')
            nuevo_tel = request.POST.get('telefono')

            if usuario_existe(nuevo_usr, exclude_personal_id=p.id):
                messages.error(request, f"⚠️ Error: El usuario '{nuevo_usr}' ya pertenece a otro registro.")
                return redirect('administrador')
            if password_existe(nueva_pwd, exclude_personal_id=p.id):
                messages.error(request, "⚠️ Error: Esa contraseña ya pertenece a otro registro.")
                return redirect('administrador')
            if telefono_existe(nuevo_tel, exclude_personal_id=p.id):
                messages.error(request, f"⚠️ Error: El teléfono '{nuevo_tel}' ya pertenece a otro registro.")
                return redirect('administrador')

            p.nombre = request.POST.get('nombre')
            p.telefono = nuevo_tel
            p.horario = f"{request.POST.get('hora_inicio')} - {request.POST.get('hora_fin')}"
            p.usuario = nuevo_usr
            p.password = nueva_pwd
            p.save()
            messages.success(request, "✅ Empleado actualizado correctamente.")

        elif accion == 'editar_paciente':
            paciente = Paciente.objects.get(id=request.POST.get('id'))
            curp_nueva = request.POST.get('curp', '').upper()
            telefono_nuevo = request.POST.get('telefono', '').strip()

            # 1. Validar longitud de CURP
            if len(curp_nueva) != 18:
                messages.error(request, '⚠️ Error: La CURP debe tener exactamente 18 caracteres.')
                return redirect('administrador')

            # 2. 📱 VALIDACIÓN DE TELÉFONO (Exactamente 10 dígitos numéricos)
            if len(telefono_nuevo) != 10 or not telefono_nuevo.isdigit():
                messages.error(request, '⚠️ Error: El teléfono debe contener exactamente 10 dígitos numéricos.')
                return redirect('administrador')
            
            # 3. Validar CURP duplicada
            if Paciente.objects.filter(curp=curp_nueva).exclude(id=paciente.id).exists():
                messages.error(request, f'⚠️ Error: La CURP "{curp_nueva}" ya pertenece a otro paciente.')
                return redirect('administrador')

            # 4. Validar Teléfono duplicado
            if telefono_nuevo != "0000000000" and Paciente.objects.filter(telefono=telefono_nuevo).exclude(id=paciente.id).exists():
                messages.error(request, f'⚠️ Error: El teléfono "{telefono_nuevo}" ya está registrado con otro paciente.')
                return redirect('administrador')

            # Guardar cambios
            paciente.nombre = request.POST.get('nombre')
            paciente.apellido_paterno = request.POST.get('apellido_paterno', paciente.apellido_paterno)
            paciente.apellido_materno = request.POST.get('apellido_materno', paciente.apellido_materno)
            
            edad_in = request.POST.get('edad')
            if edad_in and edad_in.isdigit():
                paciente.edad = int(edad_in)
            if request.POST.get('genero'):
                paciente.genero = request.POST.get('genero')

            paciente.curp = curp_nueva
            paciente.telefono = telefono_nuevo
            paciente.tipo_sangre = request.POST.get('tipo_sangre')
            paciente.save()
            messages.success(request, "✅ Paciente actualizado correctamente.")

        elif accion == 'eliminar_medico':
            Medico.objects.filter(id=request.POST.get('id')).delete()
        elif accion == 'eliminar_personal':
            Personal.objects.filter(id=request.POST.get('id')).delete()
        elif accion == 'eliminar_paciente':
            Paciente.objects.filter(id=request.POST.get('id')).delete()

        return redirect('administrador')

    contexto = {
        'medicos': Medico.objects.all(),
        'recepcionistas': Personal.objects.filter(rol='recepcion'),
        'enfermeros': Personal.objects.filter(rol='enfermeria'),
        'tecnicos': Personal.objects.filter(rol='soporte'),
        'pacientes': Paciente.objects.all(),
        'total_personal': Personal.objects.count()
    }
    return render(request, 'administrador.html', contexto)


# Módulo 7: Soporte Técnico
def soporte_vista(request):
    soporte_id = request.session.get('soporte_id')
    if not soporte_id:
        return redirect('login')
        
    tecnico_actual = Personal.objects.get(id=soporte_id)
    
    # CALCULAMOS SI ESTÁ EN TURNO USANDO LA FUNCIÓN GLOBAL
    en_turno = verificar_horario(tecnico_actual.horario)

    if request.method == 'POST':
        # Seguridad de Backend: Si no está en turno, bloqueamos cualquier intento de modificar
        if not en_turno:
            return redirect('soporte')

        accion = request.POST.get('accion')
        if accion == 'nuevo_ticket':
            TicketSoporte.objects.create(
                empleado=request.POST.get('empleado'), 
                area=request.POST.get('area'), 
                falla=request.POST.get('falla')
            )
        elif accion == 'resolver_ticket':
            ticket = TicketSoporte.objects.get(id=request.POST.get('id'))
            ticket.estado = 'Resuelto'
            ticket.resuelto_por = tecnico_actual.nombre 
            ticket.save()
        elif accion == 'eliminar_ticket':
            TicketSoporte.objects.filter(id=request.POST.get('id')).delete()
        return redirect('soporte')

    contexto = {
        'tickets': TicketSoporte.objects.all().order_by('-fecha'),
        'tecnico': tecnico_actual,
        'en_turno': en_turno 
    }
    return render(request, 'soporte.html', contexto)


# Módulo 8: Expediente de Paciente
def ver_expediente(request, id):
    try:
        paciente = Paciente.objects.get(id=id)

        consultas = Consulta.objects.filter(paciente=paciente).order_by('-fecha')
        signos = SignoVital.objects.filter(paciente=paciente).order_by('-fecha')
        
        contexto = {
            'paciente': paciente,
            'consultas': consultas,
            'signos': signos
        }
        return render(request, 'expediente.html', contexto)
    except Paciente.DoesNotExist:
        messages.error(request, "El paciente no existe.")
        return redirect('administrador')