async def generate_response(data: dict, text_normal: str = None):

    doctors_points = {
        'кардиохирургу': data.get('cardiac_surgeon_point', 0),
        'хирургу по месту жительства': data.get('surgeon_point', 0),
        'кардиологу': data.get('cardiologist_point', 0),
        'неврологу': data.get('neurologist_point', 0)
    }

    # Определяем ответы пациента по покраснению кожи и другим жалобам
    skin_redness = data.get('answer3', '')
    clicks_or_movement = data.get('answer4', '')
    discharge = data.get('answer5', '')
    fever = data.get('answer6', '')

    # Оценка по вопросам 3,4,5
    if skin_redness == 'Да, 3б.' and (clicks_or_movement == 'Да, 3б.' or discharge == 'Да, 3б.'):
        recommendation = 'кардиохирургу'
    elif skin_redness == 'Да, 3б.':
        recommendation = 'хирургу по месту жительства'
        doctors_points['кардиохирургу'] -= 3
    elif 'Да' in fever:
        if 'Да' in clicks_or_movement or 'Да' in discharge or 'Да' in skin_redness:
            recommendation = 'кардиохирургу'
    else:
        sorted_doctors = sorted(doctors_points.items(),
                                key=lambda x: x[1], reverse=True)
        recommendation = sorted_doctors[0][0]

    # Удаляем врачей, у которых баллы равны 0
    doctors_points = {doctor: points for doctor,
                      points in doctors_points.items() if points != 0}

    if not doctors_points:
        return text_normal

    sorted_doctors = sorted(doctors_points.items(),
                            key=lambda x: x[1], reverse=True)

    second_recommendation = sorted(doctors_points.items(), key=lambda x: x[1], reverse=True)[1][0] if len(
        doctors_points) > 1 and sorted_doctors[1][0] != recommendation else None  # Добавили проверку, чтобы вторая рекомендация не была такой же, как первая

    if second_recommendation:
        return f"Вам необходимо в ближайшее время записаться на консультацию к врачу <b>{recommendation}</b>.\n\n\
После посещения врача Вам рекомендовано записаться на консультацию к врачу <b>{second_recommendation}</b>.\n\n\
Записаться Вы можете, используя функцию «Записаться к врачу»"
    else:
        return f"Вам необходимо в ближайшее время записаться на консультацию к врачу <b>{recommendation}</b>.\n\
Вы можете это сделать, используя функцию «Записаться к врачу»."
