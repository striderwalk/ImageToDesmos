import cProfile
import os
import pstats

import main

with cProfile.Profile() as pr:
    main.main()

st = pstats.Stats(pr)
st.sort_stats(pstats.SortKey.TIME)


try:
    st.dump_stats(filename="output.prof")
    os.system("snakeviz ./output.prof")
except KeyboardInterrupt as e:
    pass
