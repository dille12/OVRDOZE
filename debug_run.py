import cProfile
#import RUN
import pstats
from pstats import SortKey

if input("Run game?\n>").lower() == "y":
    cProfile.run('RUN.main()', 'restats')
p = pstats.Stats('restats')

#p.print_stats()
p.sort_stats("cumtime").print_stats(100)
