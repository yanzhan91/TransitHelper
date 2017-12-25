from flask import render_template
import transithelper.RestTemplate as RestTemplate
import logging as log


def check(route, stop, agency, city_full):
    log.info('Route=%s, Stop=%s, Agency=%s, City=%s', route, stop, agency, city_full)
    city_agency = '%s-%s' % (city_full.lower().replace(' ', ''), agency.replace(' ', '-'))
    response = __get_response(route, stop, city_agency)
    if response.status_code != 200:
        log.error(response.text)
        return render_template('internal_error_message')

    try:
        data = response.json()
        minutes = data['message']['minutes']
        stop_name = data['message']['stop_name']
    except KeyError:
        log.exception(response.text)
        return render_template('internal_error_message')

    log.info('Transit api response: minutes=%s, stop_name=%s', minutes, stop_name)

    if len(minutes) == 0:
        return render_template('no_route_message', route=route, stop=stop, stop_name=stop_name)

    minute_strings = []
    for minute in minutes:
        minute_strings.append('%s minutes away <break time="200ms"/>' % minute)
    minute_string = ' and '.join(minute_strings)

    # Remove stop id if stop name exists
    if stop_name:
        stop = ''

    return render_template('check_success_message', route=route, stop=stop, minutes=minute_string, stop_name=stop_name)


def __get_response(route, stop, city_agency):
    parameters = {
        'route': route,
        'stop': stop,
        'agency': city_agency
    }
    return RestTemplate.get_response('check', parameters)
