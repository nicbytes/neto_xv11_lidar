import sys
import glob
import serial
import click

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    return ports

def check_serial_port(port):
    """ Checks if the serial port is functioning correctly

    :returns:
      True if able to connect to the serial port, otherwise false
    """
    try:
        s = serial.Serial(port)
        s.close()
        return True
    except (OSError, serial.SerialException):
        return False

class SerialInterfaceError(BaseException): pass
""" Stub class to be thrown when the serial interface has a problem. Who knows what the problem is..."""

def get_serial_interface(port, excludes=[]):
    """ Runs a small cli wizard to get a valid and available serial interface

    :raises:
      SerialInterfaceError is the selected serial interface cannot be connected to.
    :returns:
      str representing the serial interface
    """
    # select serial port
    interface = port # ensure interface is decleared outside if
    if port is None:
        ports = serial_ports()
        ports = [p for p in ports if p not in excludes]
        while True:
            for i, name in enumerate(ports):
                click.echo("({})\t{}".format(i, name))
            selection = click.prompt('Please select serial interface', type=int)
            if selection not in [i for i, n in enumerate(ports)]:
                click.echo("Error: {} is not a valid option".format(selection))
                continue
            else:
                break
        interface = ports[selection]
    # check serial interface
    if not check_serial_port(interface):
        raise SerialInterfaceError("Unable connect to: {}".format(interface))
    return interface


@click.group(invoke_without_command=True)
@click.option('--lidar-port', default=None, help='The serial file/port name (e.g. COMS4 or /dev/tty.usb3).')
@click.option('--arduino-port', default=None, help='The serial file/port name (e.g. COMS4 or /dev/tty.usb3).')
@click.pass_context
def cli(ctx, lidar_port, arduino_port):
    """ Main function run at program start.
    """
    # if there is no command, generate everything
    if ctx.invoked_subcommand is None:
        # select interfaces
        excludes = []
        if arduino_port is not None:
            excludes.append(arduino_port)
        if lidar_port is not None:
            excludes.append(lidar_port)
            click.echo("Need to select Audrino interface.")
        arduino_interface = get_serial_interface(arduino_port, excludes)
        excludes.append(arduino_port)
        if lidar_port is None:
            click.echo("Need to select Lidar interface.")
        lidar_interface = get_serial_interface(lidar_port, excludes)

if __name__ == '__main__':
    cli()
