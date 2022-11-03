import cProfile
import RUN
import pstats
from pstats import SortKey

if input("Run game?\n>").lower() == "y":
    cProfile.run('RUN.main()', 'restats')
p = pstats.Stats('restats')
p.sort_stats(SortKey.TIME).print_stats(20)
