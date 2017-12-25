from flask import render_template
import transithelper.RestTemplate as RestTemplate
import logging as log


def get(user, preset, agency, city_full):
    log.info('User=%s, Preset=%s, Agency=%s, City=%s', user, preset, agency, city_full)
    city_agency = '%s-%s' % (city_full.lower().replace(' ', ''), agency.replace(' ', '-'))
    response = __get_response(user, preset, city_agency)
    if response.status_code != 200:
        if response.json()['error_code'] == 10302:
            log.info(response.text)
            return render_template('preset_not_found_message', preset=preset, agency='%s %s' % (city_full, agency))
        else:
            log.error(response.text)
            return render_template('internal_error_message')

    data = response.json()
    try:
        minutes = data['message']['minutes']
        stop_name = data['message']['stop_name']
        route = data['message']['route']
        stop = data['message']['stop']
    except KeyError:
        log.exception(response.text)
        return render_template('internal_error_message')

    log.info('Transit api response: minutes=%s, stop_name=%s, route=%s, stop=%s', minutes, stop_name, route, stop)

    if len(minutes) == 0:
        return render_template('no_route_message', route=route, stop=stop, stop_name=stop_name)

    minute_strings = []
    for minute in minutes:
        minute_strings.append('%s minutes away <break time="200ms"/>' % minute)
    minute_string = ' and '.join(minute_strings)

    # Remove stop id if stop name exists
    if stop_name:
        stop = ''

    return render_template('check_success_message', route=route, stop=stop, minutes=minute_string,
                           stop_name=stop_name)


def __get_response(user, preset, city_agency):
    parameters = {
        'user': user,
        'preset': preset,
        'agency': city_agency
    }
    return RestTemplate.get_response('get', parameters)
