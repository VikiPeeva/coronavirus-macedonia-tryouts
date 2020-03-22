import update_data
import sys


open_data_dir = sys.argv[1]
if not open_data_dir.endswith('/'):
    open_data_dir += '/'

update_data.update_mk_covid_geojson(open_data_dir)
update_data.update_mk_covid_datasets(open_data_dir)
update_data.update_mk_covid_quarantine_geojson(open_data_dir)
update_data.update_mk_covid_summary_datasets(open_data_dir)
update_data.update_hospital_summary(open_data_dir)