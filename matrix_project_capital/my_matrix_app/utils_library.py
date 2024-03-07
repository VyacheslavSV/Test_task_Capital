import asyncio
import logging
from typing import List

import aiohttp
import requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def start_matrix_data(url):
    """
    Retrieve matrix data from the specified URL and return the parsed matrix as a list of lists of integers.

    :param url: The URL from which to retrieve the matrix data.
    :return: The parsed matrix data as a list of lists of integers.
    """
    response = requests.get(url)
    response.raise_for_status()

    matrix_text = response.text.strip()
    rows = [row.strip().split('|')[1:-1] for row in matrix_text.strip().split('\n') if row.strip()]
    start_matrix = [list(map(int, row)) for row in rows if row]
    return start_matrix


def counterclockwise_traversal(matrix):
    """
    Perform a counterclockwise traversal of the given matrix and return the result as a list.

    Args:
    matrix (list of list): The input matrix to be traversed.

    Returns:
    list: The result of counterclockwise traversal as a list.
    """
    if not matrix:
        return []

    row_start = 0
    row_end = len(matrix) - 1
    col_start = 0
    col_end = len(matrix[0]) - 1

    result = []

    while row_start <= row_end and col_start <= col_end:
        # Traverse upwards
        for row in range(row_start, row_end + 1):
            result.append(matrix[row][col_start])
        col_start += 1

        # Traverse leftwards
        for col in range(col_start, col_end + 1):
            result.append(matrix[row_end][col])
        row_end -= 1

        if col_start <= col_end:
            # Traverse downwards
            for row in range(row_end, row_start - 1, -1):
                result.append(matrix[row][col_end])
            col_end -= 1

        if row_start <= row_end:
            # Traverse rightwards
            for col in range(col_end, col_start - 1, -1):
                result.append(matrix[row_start][col])
            row_start += 1

    return result


async def get_matrix(url: str) -> List[int]:
    """
    Asynchronously fetches a matrix from the given URL and performs a counterclockwise traversal on it.
    If the server returns an error status code (>= 500 or not 200), a ValueError is raised.
    Various connection and server errors are also handled and converted to ValueErrors.
    Parameters:
        url (str): The URL to fetch the matrix from.
    Returns:
        List[int]: The result of the counterclockwise traversal on the fetched matrix.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status >= 500:
                    raise ValueError(
                        f"Server error occurred while fetching matrix from {url}. Status code: {response.status}")
                if response.status != 200:
                    raise ValueError(f"Failed to fetch matrix from {url}. Status code: {response.status}")
                text = await response.text()
                rows = [row.strip().split('|')[1:-1] for row in text.strip().split('\n') if row.strip()]
                matrix = [list(map(int, row)) for row in rows if row]

                return counterclockwise_traversal(matrix)
        except aiohttp.ClientConnectionError as e:
            logger.error(f"Failed to connect to the server at {url}. Error: {e}")
            raise ValueError(f"Failed to connect to the server at {url}. Error: {e}")
        except aiohttp.ClientResponseError as e:
            logger.error(f"Received unexpected response from the server at {url}. Error: {e}")
            raise ValueError(f"Received unexpected response from the server at {url}. Error: {e}")
        except aiohttp.ServerTimeoutError as e:
            logger.error(f"Server at {url} timed out. Error: {e}")
            raise ValueError(f"Server at {url} timed out. Error: {e}")
        except aiohttp.ServerDisconnectedError as e:
            logger.error(f"Connection to server at {url} was unexpectedly disconnected. Error: {e}")
            raise ValueError(f"Connection to server at {url} was unexpectedly disconnected. Error: {e}")
        except asyncio.TimeoutError:
            logger.error(f"Connection timeout while fetching matrix from {url}")
            raise ValueError(f"Connection timeout while fetching matrix from {url}")
        except Exception as e:
            logger.error(f"An error occurred while fetching matrix from {url}. Error: {e}")
            raise ValueError(f"An error occurred while fetching matrix from {url}. Error: {e}")


# Test the function
async def main():
    """
    This async function retrieves a matrix from the specified URL, compares it with a predefined traversal,
    and prints a success message if the comparison passes.
    """
    source_url = 'https://raw.githubusercontent.com/Real-Estate-THE-Capital/python-assignment/main/matrix.txt'
    traversal = [
        10, 50, 90, 130,
        140, 150, 160, 120,
        80, 40, 30, 20,
        60, 100, 110, 70,
    ]
    result = await get_matrix(source_url)
    assert result == traversal
    print("Test passed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
