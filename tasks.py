import invoke
import jinja2
import os
import sys
import yaml


@invoke.task()
def compile_config():
    # Parse our compile config
    with open('_compile-config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Compile each jinja2 file
    for jinja2_entry in compile_config_yaml['jinja2']['entries']:
        jinja2_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath='.'),
            undefined=jinja2.StrictUndefined
        )
        template = jinja2_environment.get_template(jinja2_entry['in'])
        with open(jinja2_entry['out'], 'w') as f:
            f.write(template.render(compile_config_yaml['config']))


@invoke.task()
def docker_machine_console():
    # Parse our compile config
    with open('_compile-config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Assemble our command
    command = 'start "{}" "{}"'.format(
        compile_config_yaml['config']['local']['docker']['cmd_bash'],
        os.path.normpath(os.path.join(os.getcwd(), 'base/docker-machine/start.sh')).replace('\\', '/'),
    )

    # Invoke it
    invoke.run(
        command,
        encoding=sys.stdout.encoding
    )


@invoke.task()
def docker_machine_ip():
    # Parse our compile config
    with open('_compile-config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Assemble our command
    command = '"{}" ip'.format(
        compile_config_yaml['config']['local']['docker']['cmd_dockermachine']
    )

    # Invoke it
    result = invoke.run(
        command,
        encoding=sys.stdout.encoding
    )


@invoke.task()
def docker_machine_purge():
    pass


@invoke.task()
def docker_machine_start(file_compose='tests/test-compose.yml'):
    # Parse our compile config
    with open('_compile-config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Assemble our command
    command = '"{}" "{}" docker-compose -f "{}" up -d'.format(
        compile_config_yaml['config']['local']['docker']['cmd_bash'],
        os.path.normpath(os.path.join(os.getcwd(), 'base/docker-machine/start.sh')).replace('\\', '/'),
        os.path.normpath(os.path.join(os.getcwd(), file_compose)).replace('\\', '/')
    )

    # Invoke it
    invoke.run(
        command,
        encoding=sys.stdout.encoding
    )


@invoke.task()
def docker_machine_stop(file_compose='tests/test-compose.yml'):
    # Parse our compile config
    with open('_compile-config.yml') as f:
        compile_config_yaml = yaml.safe_load(f)

    # Assemble our command
    command = '"{}" "{}" docker-compose -f "{}" stop'.format(
        compile_config_yaml['config']['local']['docker']['cmd_bash'],
        os.path.normpath(os.path.join(os.getcwd(), 'base/docker-machine/start.sh')).replace('\\', '/'),
        os.path.normpath(os.path.join(os.getcwd(), file_compose)).replace('\\', '/')
    )

    # Invoke it
    invoke.run(
        command,
        encoding=sys.stdout.encoding
    )


@invoke.task
def update_base():
    invoke.run('git pull https://github.com/fogies/docker-base.git master', encoding=sys.stdout.encoding)
