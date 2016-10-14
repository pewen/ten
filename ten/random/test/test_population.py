import numpy as np

from ..poblation import r_aceptors, r_nanoparticles, \
    c_aceptors, c_nanoparticles, \
    x_aceptors, x_nanoparticles


# Testing r_aceptors
def test_r_aceptors():
    """
    Testing the number of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=[2, 8], r_mechanisms=3, way='sup', sample=10)

    numbers = []
    for trap in traps:
        numbers.append(trap.number)

    check_numbers = [4, 2, 3, 5, 2, 2, 2, 7, 7, 5]
    assert(numbers == check_numbers)


def test_r_aceptors2():
    """
    Testing the r_mechanisms of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=[2, 8], r_mechanisms=[1, 3],
                       way='sup', sample=10)

    radios = []
    for trap in traps:
        radios.append(trap.r_mechanisms)

    check_radios = [2.101595805149151, 2.4162956452362097, 1.5818094778258887,
                    2.021655210395326, 2.7858939086953094, 2.792586177866876,
                    1.2511706209276725, 1.4144857562763735, 1.1029344066016598,
                    1.881619687301273]
    assert(radios == check_radios)


def test_r_aceptors3():
    """
    Testing the r_mechanisms of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=2, r_mechanisms=[1, 3],
                       way='sup', sample=10)

    radios = []
    for trap in traps:
        radios.append(trap.r_mechanisms)

    check_radios = [2.101595805149151, 2.4162956452362097, 1.5818094778258887,
                    2.021655210395326, 2.7858939086953094, 2.792586177866876,
                    1.2511706209276725, 1.4144857562763735, 1.1029344066016598,
                    1.881619687301273]
    assert(radios == check_radios)


def test_r_aceptors4():
    """
    Testing the r_mechanisms of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=[2], r_mechanisms=[1, 3],
                       way='sup', sample=10)

    radios = []
    for trap in traps:
        radios.append(trap.r_mechanisms)

    check_radios = [2.101595805149151, 2.4162956452362097, 1.5818094778258887,
                    2.021655210395326, 2.7858939086953094, 2.792586177866876,
                    1.2511706209276725, 1.4144857562763735, 1.1029344066016598,
                    1.881619687301273]
    assert(radios == check_radios)


def test_r_aceptors5():
    """
    Testing the way of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=[2, 8], r_mechanisms=[1, 3],
                       way=['sup', 'vol'], sample=10)

    ways = []
    for trap in traps:
        ways.append(trap.way)

    check_ways = ['vol', 'sup', 'vol', 'vol', 'sup',
                  'vol', 'sup', 'sup', 'vol', 'vol']
    assert(ways == check_ways)


def test_r_aceptors6():
    """
    Testing the way of traps generated.
    """
    np.random.seed(3)
    traps = r_aceptors(number=[2, 8], r_mechanisms=[1, 3],
                       way=['sup'], sample=10)

    ways = []
    for trap in traps:
        ways.append(trap.way)

    check_ways = ['sup', 'sup', 'sup', 'sup', 'sup',
                  'sup', 'sup', 'sup', 'sup', 'sup']
    assert(ways == check_ways)


# Testing r_nanoparticles
def test_r_nanoparticles():
    r_mechanisms = 15
    tau = [0.333]
    mean_path = [70, 120]
    epsilon = 1
    sample = 10
    traps = r_aceptors(number=[2, 8], r_mechanisms=[1, 3],
                       way=['sup'], sample=10)

    nanos = r_nanoparticles(r_mechanisms, tau, mean_path,
                            epsilon, traps, sample)
    assert(len(nanos) == 10)


def test_r_nanoparticles2():
    np.random.seed(2)
    r_mechanisms = 15
    tau = [0.333]
    mean_path = [70, 120]
    epsilon = 1
    sample = 10
    traps = r_aceptors(number=[2, 8], r_mechanisms=[1, 3],
                       way=['sup'], sample=10)
    nanos = r_nanoparticles(r_mechanisms, tau, mean_path,
                            epsilon, traps, sample)

    mean = []
    for nano in nanos:
        mean.append(nano.mean_path)

    check_mean = [112.69876463197444, 94.71184186909639,
                  112.3280742678734, 73.98227385045305,
                  95.2623045060852, 73.2643252193439,
                  91.40611637986947, 74.82654578303062,
                  76.35799858506387, 99.83726544892978]

    assert (check_mean == mean)


# Testing c_aceptors
def test_c_aceptors():
    number = [1, 3, 6, 9, 12, 15, 17]
    r_mechanisms = [0.3, 0.7, 1, 1.5]
    way = ['vol']

    traps = c_aceptors(number, r_mechanisms, way)
    amount_elements = len(number)*len(r_mechanisms)*len(way)
    assert(len(traps) == amount_elements)


def test_c_aceptors2():
    number = 3
    r_mechanisms = [0.3, 0.7, 1, 1.5]
    way = ['vol']

    traps = c_aceptors(number, r_mechanisms, way)
    amount_elements = len(r_mechanisms)*len(way)
    assert(len(traps) == amount_elements)


def test_c_aceptors3():
    number = [1, 3, 6, 9, 12, 15, 17]
    r_mechanisms = 0.3
    way = ['vol']

    traps = c_aceptors(number, r_mechanisms, way)
    amount_elements = len(number)*len(way)
    assert(len(traps) == amount_elements)


def test_c_aceptors4():
    number = [1, 3, 6, 9, 12, 15, 17]
    r_mechanisms = [0.3, 0.7, 1, 1.5]
    way = 'vol'

    traps = c_aceptors(number, r_mechanisms, way)
    amount_elements = len(number)*len(r_mechanisms)
    assert(len(traps) == amount_elements)


# Testing c_nanoparticle
def test_c_nanoparticle():
    number = [1, 3, 6, 9, 12, 15, 17]
    r_mechanisms = [0.3, 0.7, 1, 1.5]
    way = ['vol']
    traps = c_aceptors(number, r_mechanisms, way)

    r_np = 15
    tau = [0.333]
    mean_path = [70, 100, 120, 1500]
    epsilon = 1
    traps = traps

    nanos = c_nanoparticles(r_np, tau, mean_path, epsilon, traps)

    assert(len(nanos) == len(traps)*len(tau)*len(mean_path))


def test_c_nanoparticle2():
    number = [1, 3, 6, 9, 12, 15, 17]
    r_mechanisms = [0.3, 0.7, 1, 1.5]
    way = ['vol']
    traps = c_aceptors(number, r_mechanisms, way)

    r_np = [15, 16, 17]
    tau = 0.333
    mean_path = 70
    epsilon = 1
    traps = traps

    nanos = c_nanoparticles(r_np, tau, mean_path, epsilon, traps)

    assert(len(nanos) == len(traps)*len(r_np))


# Testing x_aceptors
def test_x_aceptors():
    numbers = [2, 12]
    r_mechanisms = [0.3, 0.7]
    ways = ['vol', 'sup']
    samples = [5, 5, 2]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    assert(len(traps) == 5*5*2)


def test_x_aceptors2():
    numbers = [2, 12]
    r_mechanisms = [0.3, 0.7]
    ways = ['vol']
    samples = 5
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    assert(len(traps) == 5*5)


def test_x_aceptors3():
    numbers = [2, 12]
    r_mechanisms = 0.3
    ways = 'vol'
    samples = [5]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    assert(len(traps) == 5)


def test_x_aceptors4():
    numbers = 2
    r_mechanisms = [0.3, 0.7]
    ways = ['vol', 'sup']
    samples = [5, 5, 2]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)
    assert(len(traps) == 5*2)


# Testing x_nanoparticles
def test_x_nanoparticles():
    numbers = [2, 12]
    r_mechanisms = [0.3, 0.7]
    ways = ['vol', 'sup']
    samples = [5, 5, 2]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)

    r_np = 15
    taus = 0.333
    mean_paths = [70, 120]
    epsilons = 1
    traps = traps
    samples = 2

    nanos = x_nanoparticles(r_np, taus, mean_paths, epsilons, traps, samples)
    assert(len(nanos) == 100)


def test_x_nanoparticles2():
    numbers = [2, 12]
    r_mechanisms = [0.3, 0.7]
    ways = ['vol', 'sup']
    samples = [5, 5, 2]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)

    r_np = 15
    taus = 0.333
    mean_paths = [70, 120]
    epsilons = 1
    traps = traps
    samples = [2]

    nanos = x_nanoparticles(r_np, taus, mean_paths, epsilons, traps, samples)
    assert(len(nanos) == 100)


def test_x_nanoparticles3():
    numbers = [2, 12]
    r_mechanisms = [0.3, 0.7]
    ways = ['vol', 'sup']
    samples = [5, 5, 2]
    traps = x_aceptors(numbers, r_mechanisms, ways, samples)

    r_np = 15
    taus = 0.333
    mean_paths = 70
    epsilons = [1, 2]
    traps = traps
    samples = 2

    nanos = x_nanoparticles(r_np, taus, mean_paths, epsilons, traps, samples)
    assert(len(nanos) == 100)