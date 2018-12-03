import csv
import numpy as np
from states import STATE_ORDER, ABBR_TO_NAME, NAME_TO_ABBR
from apportionment import oneshot_huntington_hill, iter_huntington_hill

#EPSILONS = [10**x for x in range(-1, -6, -1)]
EPSILONS = [0.01]
REPS = 100

POPULATIONS_FILE = "census_data/historical_populations.csv"
APPORTIONMENT_FILE = "census_data/house_apportionments.csv"
OUTPUT_FOLDER = "results"
VERBOSE = True

CURRENT_TESTING = True
TESTSTATE = ('MT19937', np.array([3415090279, 3511528723, 1801362174,  364455262,  182249277,
       3103951677, 3471909076,  187876718, 1846270333,  263178798,
       2372081150, 2740787819, 2825543990, 1822215401, 1675484769,
       2670361409, 2946799665, 2841550399, 2523284739, 2480364033,
       1269515935, 2015352316, 3528836812, 1261841450, 3996782142,
       1658176512, 3012521999, 1072785924, 3232093593, 2244259349,
       3525394227, 3390316295, 1416573943, 3468152330, 4139243570,
       3890210478, 3516684350, 2894157582, 2170339796, 3627549636,
       2799443195,  435691556, 1798857658, 1270979809, 3108945759,
        707009941, 2676567047, 1089235004, 3891092161, 3184440016,
       4072239199, 3224120612, 2845523031,  318883017, 1829757502,
        706381455, 3473089469, 3333365479,   85315452,  706396443,
       4215268270, 2313797778, 3654718863,  201987489, 1184538591,
       3769666915, 2055282160, 3353843801,  299440550, 3539341201,
         69645961, 1585163389, 2458612618, 4144586052, 3908650990,
       2557907679, 3309730007, 3477524043, 2262475194, 3872457394,
       1006223757, 1012367895,  627821694, 3158872885,  913838247,
       1621728673, 1898502726, 1673034936,  795990094, 1072890231,
       3322243065, 3917995968, 1728248060,  275229734,  600573961,
       3614580836, 3586971278, 3105950280, 3996469292, 2480743530,
        348465687, 1303700111, 4264912427, 2843127095, 1123117213,
       4273396986,  727498496, 3568523315, 4182983310, 1194112186,
       2884445698, 2087704165, 1987806008, 2769229273, 3557315231,
       3944493637, 3836909584, 2659319652,  811699721, 3088588195,
       2495888809, 3199616655,  399068910, 3517357482,   42896927,
       2948807259, 1147444562, 4092632720,  552841397, 3765959490,
       1577107960, 3004584140, 3831235844,  468598108, 3602304065,
       1828265046, 3548754278, 3203132215, 3145231763, 2998251044,
       3901108574, 1415509671,  800703669,   57602352, 1387821666,
       1954346062, 4234071443, 4009021974, 2793652071, 2479662613,
       1006798373, 4142875737,  298139393, 3612603930, 2643693501,
       3570778274,  162510085, 3677841198, 4130863065, 1634428092,
        298300875, 1976758689, 4284570571,  842365204, 4263203863,
       1140372137,  907675859, 3277422356,  557218552, 1774424028,
       2156438380, 3364205778, 3787603255, 3959501079,  473043448,
       2855672101,  704282137,  547636062, 3484315341, 2107984986,
        594018966, 1844602364, 3637804968,  451191602,  161185731,
       4258953811,  586119088,  292068589, 3976020499, 2697942050,
       4177431357, 3708800968, 1299282597,  525960775, 2959528777,
        945968366, 1639828155,  673856148, 3113950825, 4176513686,
       1624699690, 1228657716, 3886116464, 4060941225,  428648912,
       2181150457,  540196166, 2393947975, 4014365318, 3682793725,
        178527837,  775920849, 4197412467,  674104011, 3850514708,
        893282158, 1810442231, 2044156845, 3805613806, 4148338976,
       4235477002,  712131827, 3571932381, 4257970628, 2790517030,
       1575908574, 3827764151,  528821711, 2490133583, 3209583922,
       1112762113, 1558638225, 2945634777, 2021364549, 1943674140,
       3968095821, 1748689193,  628898569, 2115263021, 1757593448,
       3520546053, 4128118289, 3118483656, 2798554070, 1135488569,
       2858487652, 1583003810, 1091441887, 3831671598,  442425065,
       3240018622, 1886281783, 1517470517, 3622398395,   56940553,
        548042292,  688277156, 3687549162, 1547891359,  170435536,
        195311234,  739536947, 3998752597, 1513279348, 2552952776,
       1489333549, 4047340829, 2540034668, 1390822354,   91594342,
       3991090539, 3086585856, 1540034812, 4176454792, 1407872299,
       2077767890, 1629369186,  972904057, 2114268520, 2434605087,
       4022187594, 2120450962, 1737341062,  223033233, 3972434403,
       1955121390, 1271960698, 1290707281, 2046225309, 2629541480,
       4070733783, 1596584625,  955930603, 1923087030, 1296555461,
       3934808165, 3727073602,  672896746, 3529199756, 2728601868,
        528358714, 2730672600, 2444123781, 2785543281, 3351583610,
       1439855951,  874522989, 1176343881, 1602697973, 2985156904,
        515930899, 2956767514, 1387512406, 1901597207, 2930045410,
       3309464638, 3242695698,  656219573, 1704393958, 1807491737,
       1328675546,  608497234, 3864693683, 4223237925,  547141955,
        560842641,  786686603, 1288367721, 1294385954, 4279451833,
       4049399289,  828209281, 3691525917, 3554618926, 2380285348,
       2182759531,  564876628, 3748177223, 1154897373, 3892261673,
        802250958, 3687823603, 3252559084,  531181696, 2617624454,
        843118006, 3538414782, 3466226262, 2447155980, 3112116138,
       1236156913,  797975992, 2257498999, 1247289964, 3485123016,
       3483412833, 3058026382, 2600677437, 3597479857,  552530375,
       3445539236, 2423892922, 1706787772, 3049974525, 3583249878,
       3814964304, 1922980062, 2773990789,  728459145, 2779142756,
       4082277710, 2745953982, 2734117883, 3405941736, 4056562702,
        452707453, 1769164042, 2840580789, 1133178778, 3804264194,
       1170515597, 1802159105, 1841009425, 3263657696, 1398904410,
       3475010151, 1158722522, 2049947315, 4162416266,  174915035,
       3227517327,  422720763, 3515027298, 2608127253,  267945220,
       2259288126, 3749020033,  550294133, 2889554254, 3640753526,
       1177280583, 3572462874, 2789561401, 4232221621, 1054273055,
       2826195556,   92810568, 2240915674, 4142848849,  100179379,
       1630662137, 2727763009, 3376191923, 2355087771, 3374281257,
       3832632556, 1353057707, 3885054219,  761677388, 3307162677,
       2750566843,  311581440,  248867994, 2201996226, 1851353074,
        366577448, 1406666023, 1919519218, 3180547307,  149019699,
       1383500787, 2257613762,  772093405, 4003588569, 2296968102,
       2608598851, 1362705380, 1762537146,  649337625, 3937504617,
        179786448,  528070756, 1564574054, 2433665791, 3209352051,
        808230031, 2081042348, 3248108567, 2002669077, 1321532392,
       4090527447, 1095078060,  853124779, 1503799872,  163903767,
       1305841671, 4067212849, 1835735396, 1621561372, 2305007390,
       1991038554, 1931855683, 1879080464, 2931595026, 1703625168,
        119576252,  275368966, 2695091393, 2836267716, 3448136041,
       3532500815, 2411527087, 3033598654, 3555175102,   22694712,
       2308988581, 3501119976, 3091177864, 2424220807, 1288975919,
       1389475728, 3765930847, 2144723681, 2128536947, 3113918543,
        764993451, 1087334330, 2453426410, 3088998745, 1332969630,
       1260132194, 4259584873, 3955136782, 1210704255, 2952446112,
       1451819905, 3275833630, 3186999364, 1815114322, 3237004326,
       3175946352,  235455948, 3096835189, 4105568670, 4131466724,
       1702198958, 3309709398, 3636036495, 2741707258, 1908643288,
       2049592273,  109662957, 3254780979, 3613547463, 3538652317,
       3101813756, 3211099139, 2010155665, 1881232901, 4140539591,
        426037065, 2720540743, 2029037390, 1955536977, 1730093483,
       3828665249,  482874266,  690406101, 1897463070, 3184507783,
       1880304913, 1498445634,  641142039,  744396644, 3531345700,
        818707479,  142464517, 2513390864,   81066145, 1753256627,
       2593233028, 4109633218, 1384864579, 1512563599, 2529394514,
       2533455308, 2180246417, 3003587534, 2201411017, 2975161432,
       1574447474,  861418041, 2700659909,  874208205, 3160356252,
        520041300, 3457041584, 2757567999, 1167127807, 2873464501,
       2721870398,  711060637, 2115061203, 1374113539, 1443044552,
       3840000131,  431735249, 3740480463, 3741700677,  130089183,
       2078253688, 3314049136, 1692161774, 1925303015, 3937065603,
       2528215742, 2244990616, 2140935344, 3786343664, 4225746894,
       1935579150, 1900837919, 3952414477, 2678965031, 3726614189,
       1688918037, 1639009859, 1278139103, 3494154820,  866528038,
       3868196218,  994335358,  561079451, 2428209291, 3171913381,
       1135308324,  401493718, 2756456190, 1714877353, 3985150744,
       4237353323, 2872980267,  542790283, 1030371873, 1235860178,
       1066839504, 4046048365,  532640275, 2718285380, 2629737625,
       2436937750,  757620311, 2418259105, 3102848590, 1974720661,
       1412829143,  475112692, 3758715185,  272192991, 3696320640,
       1381794463,  274783425,   45904949,  599401325], dtype=np.uint32), 72, 0, 0.0)

#########################################################
# Parsing functions
#########################################################

def parse_historical_populations(filename=POPULATIONS_FILE):
    census_years = []
    total_us_pop = []
    state_pops = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        # parse first row separately
        census_years = list(map(int, next(reader)[1:-3]))
        total_us_pop = dict(zip(census_years, list(map(int, next(reader)[1:-3]))))
        state_pops = dict()

        for row in reader:
            name = row[0]
            abbr = NAME_TO_ABBR[name]

            # Manually skip District of Columbia becasue they don't have seats in the house
            if abbr == 'DC':
                continue

            for i in range(len(row[1:-3])):
                year = census_years[i]
                popstr = row[1:-3][i]
                if year not in state_pops.keys():
                    state_pops[year] = dict()
                state_pops[year][abbr] = None if len(popstr)==0 else int(popstr)

    return set(census_years), total_us_pop, state_pops

def parse_historical_seats_apportioned(filename=APPORTIONMENT_FILE):
    census_years = []
    total_seats_apportioned = []
    state_seats_apportioned = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        census_years = list(map(int, next(reader)[1:]))
        total_seats_apportioned = { year: 0 for year in census_years }
        state_seats_apportioned = { year: dict() for year in census_years }
        for row in reader:
            name = row[0]
            for i in range(len(row[1:])):
                year = census_years[i]
                seats = row[1:][i]
                state_seats_apportioned[year][name] = None if seats=='-' else int(seats)
                total_seats_apportioned[year] += 0 if seats=='-' else int(seats)

    # Manually add 1920 (equal to 1910 reult) and 2017 (equal to 2010 result)
    census_years.append(1920)
    census_years.append(2017)
    census_years.sort()

    total_seats_apportioned[1920] = total_seats_apportioned[1910]
    total_seats_apportioned[2017] = total_seats_apportioned[2010]

    state_seats_apportioned[1920] = dict(state_seats_apportioned[1910])
    state_seats_apportioned[2017] = dict(state_seats_apportioned[2010])

    return set(census_years), total_seats_apportioned, state_seats_apportioned

#########################################################
# Experiments
#########################################################

# TEMPORARY NOISE FUNCTION
def laplace_noise(dims, epsilon):
    # 1/epsilon because GS of count is 1
    return np.random.laplace(scale= 1/epsilon, size = dims)

def run_experiment():
    # Writes a function that returns the changes that must be made TO THE TRUE APPORTIONMENT in order to equal the
    # NOISY RESULT

    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)

    for year in census_years:
        if CURRENT_TESTING:
            if year != 1930:
                continue
        print("year: ", str(year))
        if VERBOSE: print("=================================")

        true_population = total_us_pop[year]
        true_state_pop = state_pops[year]
        true_seats = total_seats_apportioned[year]

        true_answer_ones = oneshot_huntington_hill(true_population, true_state_pop, true_seats)
        true_answer_iter = iter_huntington_hill(true_population, true_state_pop, true_seats)
        assert(true_answer_ones == true_answer_iter)
        true_answer = true_answer_iter

        if any(count is None for count in true_state_pop.values()):
            if VERBOSE: print("Not doing year %d because there is a None count" % year)
            continue

        with open(OUTPUT_FOLDER + "/" + str(year) + ".csv", 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["epsilon", "rep"] + STATE_ORDER)

            for epsilon in EPSILONS:
                print("  epsilon: ", str(epsilon))
                if VERBOSE: print("---------------------------------")

                for rep in range(REPS):
                    if CURRENT_TESTING:
                        if rep != 6:
                            continue
                        #print("State for next rep:")
                        #print(np.random.get_state())
                        np.random.set_state(TESTSTATE)

                    noises = laplace_noise(len(true_state_pop), epsilon)
                    population = true_population + sum(noises)
                    state_pop = dict()
                    for (state, i) in zip(true_state_pop.keys(), range(len(true_state_pop))):
                        state_pop[state] = true_state_pop[state] + noises[i]
                    answer_iter = iter_huntington_hill(population, state_pop, true_seats)

                    answer = answer_iter
                    if true_answer != answer:
                        if VERBOSE: print("iter method: epsilon: %f, year: %d, rep: %d, Different" % (epsilon, year, rep))
                        for state in true_answer:
                            if true_answer[state] != answer[state]:
                                diff = answer[state] - true_answer[state]
                                if VERBOSE: print("    ", state, "+" if diff > 0 else " " if diff == 0 else "", diff)
                    else:
                        if VERBOSE: print("iter method: epsilon: %f, year: %d, rep: %d, Same" % (epsilon, year, rep))

                    answer_ones = oneshot_huntington_hill(population, state_pop, true_seats)
                    if answer_iter != answer_ones:
                        print("DIFFERENCE BETWEEN HH ITER AND ONESHOT METHOD")
                        for state in answer_iter:
                            if answer_iter[state] != answer_ones[state]:
                                diff = answer_iter[state] - answer_ones[state]
                                if VERBOSE: print("    ", state, "iter: ", answer_iter[state], "ones: ", answer_ones[state])
                    answer = answer_ones
                    writer.writerow([epsilon, rep] + [answer[st] - true_answer[st] for st in STATE_ORDER])
                    if true_answer != answer:
                        if VERBOSE: print("ones method: epsilon: %f, year: %d, rep: %d, Different" % (epsilon, year, rep))
                        for state in true_answer:
                            if true_answer[state] != answer[state]:
                                diff = answer[state] - true_answer[state]
                                if VERBOSE: print("    ", state, "+" if diff > 0 else " " if diff == 0 else "", diff)
                    else:
                        if VERBOSE: print("ones method: epsilon: %f, year: %d, rep: %d, Same" % (epsilon, year, rep))
    print("Done!  Results are in ", OUTPUT_FOLDER)


if __name__ == '__main__':
    census_years, total_us_pop, state_pops = parse_historical_populations(POPULATIONS_FILE)
    census_years, total_seats_apportioned, state_seats_apportioned = parse_historical_seats_apportioned(APPORTIONMENT_FILE)

    run_experiment()

    #print(census_years)
    #print(total_seats_apportioned)
    #print(state_seats_apportioned)

