import pickle

def save_coefficients(mtx, dist, path) -> None:
    with open(f'{path}/coefficients.p', 'wb') as f:
        coef = {'mtx': mtx, 'dist': dist}
        pickle.dump(coef, f)

def load_coefficients(path) -> tuple:
    '''Reads the coefficients from a path and return it.\n
    - Return: tuple(mtx, dist)'''

    with open(f'{path}/coefficients.p', 'rb') as f:
        coef = pickle.load(f)
    return coef['mtx'], coef['dist']