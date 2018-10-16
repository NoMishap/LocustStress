from subprocess import call


def call_locust(options):
    file = "src/locust_files/" + options['file']['value']
    host = "--host=" + options['host']['value']
    output = "--csv=" + options['output']['value']

    params = list(["locust", "-f", file, host, output])

    if options['no_web']['value'] is not False:
        params.append('--no-web')

    if options['num_call']['value'] != 0:
        params.append('-c')
        params.append(str(options['num_call']['value']))

    if options['users_for_second']['value'] != 0:
        params.append('-r')
        params.append(str(options['users_for_second']['value']))

    if options['time']['value'] is not None:
        params.append('-t' + options['time']['value'])

    call(params)


def call_locust_master(options):
    file = "src/locust_files/" + options['file']['value']
    host = "--host=" + options['host']['value']
    output = "--csv=" + options['output']['value']

    params = list(["locust", "-f", file, "--master", host, output])

    if options['no_web']['value'] is not False:
        params.append('--no-web')

    if options['num_call']['value'] != 0:
        params.append('-c')
        params.append(str(options['num_call']['value']))

    if options['users_for_second']['value'] != 0:
        params.append('-r')
        params.append(str(options['users_for_second']['value']))

    if options['time']['value'] is not None:
        params.append('-t' + options['time']['value'])

    if options['slaves']['value'] is not None:
        params.append('--expect-slaves=' + options['slaves']['value'])

    call(params)


def call_locust_slave(options):
    file = "src/locust_files/" + options['file']['value']
    master_host = options['master_host']['value']
    output = "--csv=" + options['output']['value']

    params = list(["locust", "-f", file, "--slave", output, "--master-host=" + master_host])

    call(params)
