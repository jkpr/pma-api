"""Performance checks."""
import os
from datetime import datetime
from glob import glob
from subprocess import call
from collections import OrderedDict

import manage
from pma_api.models import Data


TEST_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
TEST_FILES_DIR = TEST_DIR + 'files/'


class CheckPerformance:
    """Test performance."""

    @staticmethod
    def output_for_r(seconds_by_n_rows):
        """Output to be read by R for plotting.

        Args:
            seconds_by_n_rows (dict): Seconds elapsed for creation of database
                by 'n' sized input rows.
        """
        sorted_seconds_by_n_rows = \
            OrderedDict(sorted(seconds_by_n_rows.items()))
        n, seconds = \
            [k for k in sorted_seconds_by_n_rows], \
            [v for k, v in sorted_seconds_by_n_rows.items()]
        output_for_r = str(
            "# Actual time elapsed by 'n': 'seconds' (for 'R'): \n\n" +
            "n <- c" + str(n) + "\n" +
            "seconds <- c" + str(seconds) + "\n" +
            "plot(n, seconds)"
        ).replace('[', '(').replace(']', ')')

        filename = 'db_create_performance_' + \
                   str(datetime.now()).replace('/', '.').replace('.', '-')\
                   + '.R'
        _file = TEST_FILES_DIR + '/data/ignored/output/' + filename

        call(['touch', _file])
        with open(_file, 'w') as file:
            file.write(output_for_r)

    @staticmethod
    def check_create_db():
        """Check performance of DB creation.

        Result is a dictionary 'seconds_by_n_rows', of seconds elapsed for
        creation of database by 'n' sized input rows.

        # TODO (1): 2017/11/30-jef, Instead of messing with initdb, perhaps I
        # can just call the function init_wb and pass it the app and only
        # the worksheet, and skip the caching. That way I can possibly
        # avoid gunking up manage.py and config.py.

        # TODO (2): 2017/11/30-jef, Rather than have explicit files with set
        # number of data rows, possibly modify the resulting WB objects.

        # TODO (3): 2017/11/30-jef, If feasible with small 'n' samples given
        # noise of lower order terms, estimate o(N) by comparing slopes between
        # separate seconds/n observations, to ascertain how the slope is
        # changing. Then set a threshold for desirable complexity and set a
        # test to ensure that the threshold is not exceeded.
        """
        os.environ['FLASK_CONFIG'] = 'test'
        src_dir = TEST_FILES_DIR + 'data/'
        src_files = glob(src_dir + 'api_data*.xlsx')
        seconds_by_n_rows = {}

        for file in src_files:
            manage.API_DATA = file
            t0 = datetime.now()
            manage.initdb(overwrite=True, test=True)  # (1)
            t1 = datetime.now()

            with manage.app.app_context():
                result = Data.query.all()

            seconds_by_n_rows[len(result)] = (t1 - t0).seconds

        CheckPerformance.output_for_r(seconds_by_n_rows)


if __name__ == '__main__':
    CheckPerformance.check_create_db()
