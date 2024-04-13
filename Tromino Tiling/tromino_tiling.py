import sys
from plot_table import plot


def check_args():
    """
    Check if the only one parameter has been passed through the args and if it's a number or not
    :return: The number passed from the args
    """

    # Ensure exactly one argument is provided
    if len(sys.argv) != 2:
        print("The number of arguments needed are 1.", file=sys.stderr)
        sys.exit(1)

    # Try to convert the argument to an integer
    try:
        number = int(sys.argv[1])
        return number
    except ValueError:
        print("You must provide an integer for dimensions of the table.", file=sys.stderr)
        sys.exit(1)


def create_pw_sqr_table(dim: int):
    """
    A method that creates the 2D table with shape 2^N * 2^N that we are called to fill with trominos
    :param dim: The N number passed from the cmd
    :return: A 2D table with dimensions of 2^dim * 2^dim
    """
    return [['X' for _ in range(2 ** dim)] for _ in range(2 ** dim)]


def check_if_corners_are_empty(table, log, lat, r):
    """
    Check which corner is not empty to know the direction of the trominos that we will place
    Args:
        :param table: The table we need to fill.
        :param log: Row index of the top left corner of the sub-table.
        :param lat: Column index of the top left corner of the sub-table.
        :param r: Size of the sub-table.
    :return:
        0 if the corners are empty, 1,2,3,4, according to the place that it will find the direction.
        If it finds the upper right corner not empty, it returns 4. Why 4?
        We want to return the number of the opposite corner of the table to know how to place the trominos.
    """

    # Upper left check
    if table[log][lat] != 'X':
        return 3

    # Upper right check
    elif table[log][lat + r - 1] != 'X':
        return 4

    # Bottom left check
    elif table[log + r - 1][lat] != 'X':
        return 2

    # Bottom right check
    elif table[log + r - 1][lat + r - 1] != 'X':
        return 1

    # All corners are empty
    else:
        return 0


def place_central_tromino(table: list, direction=3, log=0, lat=0, r=0):
    """
    According to the direction place the central tromino with green color. \n
    Direction 1: Upper left \n
    Direction 2: Upper right \n
    Direction 3: Bottom right \n
    Direction 4: Bottom left \n

    :param r: Size of the sub-table.
    :param lat: Column index of the top left corner of the sub-table.
    :param log: Row index of the top left corner of the sub-table.
    :param table: The table we need to fill.
    :param direction: The direction of the tromino's noise
    """

    # Find the center of the table
    center = find_table_center(log, lat, r)

    # Place the tromino in the specific cell according to the direction
    # Upper left direction
    if direction == 1:
        table[center[0][0]][center[0][1]], table[center[1][0]][center[1][1]], table[center[2][0]][
            center[2][1]] = 'G', 'G', 'G'

    # Upper right direction
    elif direction == 2:
        table[center[0][0]][center[0][1]], table[center[1][0]][center[1][1]], table[center[3][0]][
            center[3][1]] = 'G', 'G', 'G'

    # Bottom right direction
    elif direction == 3:
        table[center[1][0]][center[1][1]], table[center[2][0]][center[2][1]], table[center[3][0]][
            center[3][1]] = 'G', 'G', 'G'

    # Bottom left direction
    else:
        table[center[0][0]][center[0][1]], table[center[2][0]][center[2][1]], table[center[3][0]][
            center[3][1]] = 'G', 'G', 'G'


def find_table_center(log, lat, r):
    """
    :param r: Size of the sub-table.
    :param lat: Column index of the top left corner of the sub-table.
    :param log: Row index of the top left corner of the sub-table.
    :return: The indixes of the central 4 cells that make up the central point
    """

    # Find the center point and return the neighbor cells
    center = r // 2
    return [(center - 1 + log, center - 1 + lat), (center - 1 + log, center + lat), (center + log, center - 1 + lat), (center + log, center + lat)]


def fill(table, log, lat, direction):
    """
    The method that will fill the 2^2 * 2^2 sub-table. This method will fill the 4*4 table
    according to the direction we placed the central tromino. The color will be as following:

    - Upper left: Blue
    - Upper right: Red
    - Bottom right: Blue
    - Bottom left: Red

    :param table: The table we need to fill.
    :param log: Row index of the top left corner of the sub-table.
    :param lat: Column index of the top left corner of the sub-table.
    :param direction: The direction of the tromino's noise
    """
    if direction in (0, 1):
        # Upper left
        table[log][lat], table[log + 1][lat], table[log][lat + 1] = 'B', 'B', 'B'
        # Bottom right
        table[log + 2][lat + 2], table[log + 3][lat + 2], table[log + 2][lat + 3] = 'B', 'B', 'B'

        # Bottom left
        table[log + 2][lat], table[log + 3][lat], table[log + 3][lat + 1] = 'R', 'R', 'R'
        # Upper right
        table[log][lat + 2], table[log][lat + 3], table[log + 1][lat + 3] = 'R', 'R', 'R'

    elif direction == 2:
        # Upper left
        table[log][lat], table[log + 1][lat], table[log][lat + 1] = 'B', 'B', 'B'
        # Bottom right
        table[log + 3][lat + 3], table[log + 3][lat + 2], table[log + 2][lat + 3] = 'B', 'B', 'B'

        # Bottom left
        table[log + 2][lat], table[log + 2][lat + 1], table[log + 3][lat + 1] = 'R', 'R', 'R'
        # Upper right
        table[log][lat + 2], table[log][lat + 3], table[log + 1][lat + 3] = 'R', 'R', 'R'

    elif direction == 3:
        # Upper left
        table[log + 1][lat + 1], table[log + 1][lat], table[log][lat + 1] = 'B', 'B', 'B'
        # Bottom right
        table[log + 3][lat + 3], table[log + 3][lat + 2], table[log + 2][lat + 3] = 'B', 'B', 'B'

        # Upper right
        table[log][lat + 2], table[log][lat + 3], table[log + 1][lat + 3] = 'R', 'R', 'R'
        # Bottom left
        table[log + 2][lat], table[log + 3][lat], table[log + 3][lat + 1] = 'R', 'R', 'R'

    else:
        # Upper left
        table[log][lat], table[log + 1][lat], table[log][lat + 1] = 'B', 'B', 'B'
        # Bottom right
        table[log + 3][lat + 3], table[log + 3][lat + 2], table[log + 2][lat + 3] = 'B', 'B', 'B'

        # Bottom left
        table[log + 2][lat], table[log + 3][lat], table[log + 3][lat + 1] = 'R', 'R', 'R'
        # Upper right
        table[log][lat + 2], table[log + 1][lat + 2], table[log + 1][lat + 3] = 'R', 'R', 'R'


def tromino_tiling(table, log, lat, r):
    """
    The main algorithm that will work recursively to fill the table with L shaped trominos.

    :param table: The table we need to fill.
    :param log: Row index of the top left corner of the sub-table.
    :param lat: Column index of the top left corner of the sub-table.
    :param r: Size of the sub-table.
    """

    # Check first the length of the table to know if we should split the table of fill
    # If the length of the table if greater than 4 we place a tromino in the center and we split.
    if r > 4:
        # Check for the direction of the central tromino that we should place
        direction = check_if_corners_are_empty(table, log, lat, r)

        # According to the direction, place the tromino
        if direction == 0:
            place_central_tromino(table, 3, log, lat, r)
        else:
            place_central_tromino(table, direction, log, lat, r)

        # Callback tromino tilling but update the log, lat according to the quarter that we are aiming
        new_r = r // 2
        tromino_tiling(table, log, lat, new_r)
        tromino_tiling(table, log, lat + new_r, new_r)
        tromino_tiling(table, log + new_r, lat, new_r)
        tromino_tiling(table, log + new_r, lat + new_r, new_r)

    # If the table is 2^2 * 2^2 then we place one in the center and fill the rest of the sub-table.
    elif r == 4:
        # Check for the direction of the central tromino that we should place
        direction = check_if_corners_are_empty(table, log, lat, r)

        # According to the direction, place the tromino
        if direction == 0:
            place_central_tromino(table, 1, log, lat, r)
        else:
            place_central_tromino(table, direction, log, lat, r)

        # Fill the table with the rest of the trominos because we are in a 2^2 * 2^2 sub-table.
        fill(table, log, lat, direction)

    # If the table's length is not 4*4 or greater than that,
    # this mean the n=1, so we just place a tromino in the center and break
    else:
        place_central_tromino(table, 4, 0, 0, 2)


if __name__ == "__main__":
    # Check the args for the n number given from the cmd
    n = check_args()

    # Create a table with dimensions 2^n * 2^n
    n_power_table = create_pw_sqr_table(n)

    # Run the tromino tiling callback
    tromino_tiling(n_power_table, 0, 0, len(n_power_table))

    # Print the filled table
    for row in n_power_table:
        print(row)

    plot(n_power_table)
