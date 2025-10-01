#
# Copyright Kroxylicious Authors.
#
# Licensed under the Apache Software License version 2.0, available at http://www.apache.org/licenses/LICENSE-2.0
#

def sasl_conf(args):
    sasl_mechanism = args.sasl_mechanism

    sasl_config = {'sasl.mechanism': sasl_mechanism,
                   'security.protocol': args.security_protocol}

    if sasl_mechanism != 'GSSAPI':
        sasl_config.update({'sasl.username': args.username,
                            'sasl.password': args.user_secret})

    if sasl_mechanism == 'GSSAPI':
        sasl_config.update({'sasl.kerberos.service.name', args.broker_principal,
                            # Keytabs are not supported on Windows. Instead,
                            # the logged on user's credentials are used to authenticate.
                            'sasl.kerberos.principal', args.username,
                            'sasl.kerberos.keytab', args.user_secret})
    return sasl_config
