""" Speed-IT
"""
from os.path import abspath as path_abspath
from sys import exit as sys_exit

# Import speed_it
try:
   # noinspection PyPackageRequirements,PyUnresolvedReferences
   from PySpeedIT.speed_it import speed_it
except ImportError as err:
   sys_exit('''
      Example SpeedTest: Can not run speed_it. This module needs the package <PySpeedIT >= 1.0.6> to be installed: <{}>
      '''.format(err)
   )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # defining the: modules_func_tuple mapping
   modules__func_tuples = (
      # TUPLE format:
      # [module_path_str, ((name_str, function_name_str, list_of_positional_arguments, dictionary_of_keyword_arguments))]
      [path_abspath('emit_lconf_json1.py'), (
         ('do_emit__lconf', 'do_emit__lconf', [], {}),
         ('do_emit__json_ordered', 'do_emit__json_ordered', [], {}),
         ('do_emit__json', 'do_emit__json', [], {}),
      )],
      [path_abspath('parse_lconf_json1.py'), (
         ('do_parse__lconf', 'do_parse__lconf', [], {}),
         ('do_parse__json_ordered', 'do_parse__json_ordered', [], {}),
         ('do_parse__json', 'do_parse__json', [], {}),
      )],
   )

   speed_it(
      html_output_dir_path=path_abspath('result_output_speed_it_lconf_json'),
      enable_benchmarkit=True,
      enable_profileit=False,
      enable_linememoryprofileit=False,
      enable_disassembleit=False,
      modules__func_tuples=modules__func_tuples,
      output_max_slashes_fileinfo=2,
      use_func_name=True,
      output_in_sec=False,
      profileit__repeat=1,
      benchmarkit__output_source=False,
      benchmarkit__with_gc=False,
      benchmarkit__check_too_fast=True,
      benchmarkit__rank_by='worst',
      benchmarkit__run_sec=2.0,
      benchmarkit__repeat=3
   )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
