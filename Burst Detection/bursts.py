import sys
from Bellman_Ford import Bellman_Ford
from Viterbi import BurstViterbi


def args_error_handle(s, gamma, algo_name, filename):
    """
    A method that checks the correctness of the parameters given in the args.

    :param gamma: The gamma parameter from the args.
    :param s: The s parameter from the args.
    :param algo_name: The algorithm name from the args.
    :param filename: The file name from the args
    :return: If the algorithm or filename is empty,
    or number of parameters passed are more than 8 throw Exception with the appropriate message.
    """

    # Initialize an error message
    error_mess = '\n\n**  Error in the parameters you passed:  **\n\n'
    count = 1

    # Check if the file name is empty or not.
    if filename == '':
        error_mess += f'{count}) You must pass a file name!\n'
        count += 1

    # Check if the algorithm name is empty or not.
    if algo_name == '':
        error_mess += f'{count}) You must define an algorithm to use, viterbi or trellis!\n'
        count += 1

    # If a value has been given to the s parameter, then this is passed as a string, so let's parse it to numeric.
    if isinstance(s, str):
        try:
            s = float(s)

            # s parameter must not be 1, otherwise we can't calculate important parameters of the program (like K).
            if s <= 1:
                raise ValueError()
        except ValueError:
            error_mess += f'{count}) The s parameter must be numeric not string and greater than 1! \n'
            count += 1

    # If a value has been given to the g parameter, then this is passed as a string, so let's parse it to numeric.
    if isinstance(gamma, str):
        try:
            gamma = float(gamma)

            # gamma parameter must be bigger than 1
            if gamma <= 0:
                raise ZeroDivisionError()
        except ValueError:
            error_mess += f'{count}) The g parameter must be numeric not string! \n'
            count += 1
        except ZeroDivisionError:
            error_mess += f"{count}) The gamma parameter must be greater than 0! \n"
            count += 1

    # Check if the user passed too many args.
    if len(sys.argv) > 8:
        error_mess += (f'{count}) You passed more arguments than you should! \n'
                       f'   The arguments you can define is s, gamma, d, algorithm and filename\n')
        count += 1

    # If even one condition is true, then throw an exception to stop the program, else return s and g as numeric.
    if count > 1:
        raise Exception(error_mess)
    else:
        return s, gamma


def check_args():
    """
    Check the args to take the parameters needed to run the program.

    :return: The type of algorithm, the file name, set a new value on s and gamma, and if the user passed the d param
    """

    # Initialize the parameters we need
    s = 2
    gamma = 1
    file_name = ''
    algorithm = ''
    d = False

    # Check the args and extract each parameter that we need and are passed
    for i in range(len(sys.argv)):

        # Check for the -d parameter
        if sys.argv[i] == '-d':
            d = True

        # Check for the -s parameter
        elif sys.argv[i] == '-s':
            # Check if the user has entered the -s parameter in the end and didn't pass a value
            try:
                s = sys.argv[i + 1]
            except IndexError:
                print('**  Error in the parameters you passed:  **\n')
                print('1) After the -s parameter you must pass the number.')
                exit(0)

        # Check for the -g parameter
        elif sys.argv[i] == '-g':
            # Check if the user has entered the -g parameter in the end and didn't pass a value
            try:
                gamma = sys.argv[i + 1]
            except IndexError:
                print('**  Error in the parameters you passed:  **\n')
                print('1) After the -g parameter you must pass the number.')
                exit(0)

        # Check for the algorithm name parameter
        elif sys.argv[i] in ['viterbi', 'trellis']:
            algorithm = sys.argv[i]

        # Check for the file name parameter
        elif sys.argv[i][-4:] == '.txt':
            file_name = sys.argv[i]

    # Check for exception in the args
    try:
        s, gamma = args_error_handle(s, gamma, algorithm, file_name)
    except Exception as ex:
        print(ex)
        exit(0)

    return s, gamma, file_name, algorithm, d


def read_file(filename):
    """
    A method that will read the file data and returns them in a structure format.

    :param filename: The file path.
    :return: An array with the data.
    """

    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            line = file.readline()
            numbers = line.split()

            if filename in ['three_states_1.txt', 'two_states.txt']:
                times = [int(number) for number in numbers]
            else:
                times = [float(number) for number in numbers]

            return times
    except ValueError:
        print("Error: The file contains non-numeric values.")
        exit(0)


if __name__ == "__main__":
    # Check the args to take the parameters needed
    s, gamma, filename, algo_name, d = check_args()

    # Extract the times from the file
    times = read_file(filename)

    # Run the appropriate algorithm to find the optimal path
    if algo_name == 'viterbi':
        algo = BurstViterbi(times, s, gamma)
    else:
        algo = Bellman_Ford(times, s, gamma)

    algo.results(d)
