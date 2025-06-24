def plantilla_sms_cancelacion(receptor, reserva):
    if receptor == 'medico':
        return f"Se ha cancelado la reserva del paciente {reserva.paciente.nombre_completo} programada para el {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')}."
    elif receptor == 'paciente':
        return f"Tu cita con el Dr. {reserva.medico.nombre_completo} el {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')} ha sido cancelada."
    return ""

def plantilla_sms_completada(receptor, reserva):
    if receptor == 'paciente':
        return f"Gracias por asistir a tu cita con el Dr. {reserva.medico.nombre_completo}. Tu atención fue registrada como completada."
    elif receptor == 'medico':
        return f"La consulta con el paciente {reserva.paciente.nombre_completo} fue marcada como completada."
    return ""
